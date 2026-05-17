import time
import requests
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import alpaca_trade_api as tradeapi
import google.generativeai as genai
from bs4 import BeautifulSoup
import urllib.parse

# ==========================================
# ⚙️ SALVADOR YAZILIM KONTROL MERKEZİ ⚙️
# ==========================================

TELEGRAM_TOKEN = "8999614534:AAFcDigxTM8ck2j_2Gh73n-l_Ysyiz-C9fY"
ADMIN_CHAT_ID = "1797520280" 
IZINLI_KULLANICILAR = ["1797520280", "1406338226"]

GEMINI_API_KEY = "AIzaSyDWDMCQ_hNRpJxYLti5caMn8ovMgPhe760"
genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel('gemini-2.5-flash')

ALPACA_API_KEY = "PK7PYTIBJLKNGUCXZQ63XGB3SF"
ALPACA_SECRET_KEY = "2VnQRsfpWygmHMKQe4qgwpjhrE54AZAnsbY7eitBcYG3"
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version='v2')

# ==========================================
# 🛠️ ÇEKİRDEK FONKSİYONLAR
# ==========================================

def telegram_mesaj_gonder(chat_id, metin, butonlar=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": metin, "parse_mode": "Markdown"}
    if butonlar:
        payload["reply_markup"] = {"inline_keyboard": butonlar}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Telegram Mesaj Gönderme Hatası:", e)

def hisse_kodu_hazirla(kod):
    """
    Girilen kodu analiz eder ve US veya BIST hissesi olduğunu belirler.
    """
    kod = kod.upper().strip()
    if len(kod) >= 4 and kod.startswith(("AAPL", "TSLA", "MSFT", "NVDA", "AMZN", "GOOG")):
        return "US", kod
    if not kod.endswith(".IS"):
        return "BIST", f"{kod}.IS"
    return "BIST", kod

def pazar_gunu_guvenli_veri_cekici(hisse):
    """
    Google News RSS ve Yahoo Finance üzerinden verileri toplayan koruma köprüsü.
    """
    tip, analiz_kodu = hisse_kodu_hazirla(hisse)
    veri = {"fiyat": None, "haberler_ham": ""}
    
    # 1. Aşama: Google News RSS Üzerinden Kararlı Haber Çekimi
    try:
        arama_terimi = f"{hisse} hisse haber" if tip == "BIST" else f"{hisse} stock news"
        url_kodlu = urllib.parse.quote(arama_terimi)
        rss_url = f"https://news.google.com/rss/search?q={url_kodlu}&hl=tr&gl=TR&ceid=TR:tr"
        
        response = requests.get(rss_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")
            
            if items:
                başlıklar = []
                for item in items[:6]:
                    başlıklar.append(f"- {item.title.text}")
                veri["haberler_ham"] = "\n".join(başlıklar)
            else:
                veri["haberler_ham"] = f"{hisse} hakkında yakın zamanda sisteme düşen majör bir haber akışı bulunamadı."
        else:
            veri["haberler_ham"] = "Haber sunucusu şu an yoğun, genel piyasa beklentisi üzerinden yorumlanacak."
    except Exception as e:
        print(f"Google News Scraper Hatası: {e}")
        veri["haberler_ham"] = "Haber akışı şu an için çekilemedi, genel teknik trend baz alınacak."

    # 2. Aşama: Hızlı Fiyat Çekimi
    try:
        df = yf.download(tickers=analiz_kodu, period="7d", interval="1d", progress=False)
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
                
            veri["fiyat"] = float(df['Close'].values[-1])
            veri["dip"] = float(df['Low'].values[-1])
            veri["tepe"] = float(df['High'].values[-1])
            return veri
    except Exception as e:
        print(f"Yahoo Fiyat Çekim Hatası: {e}")
        
    return None

def detayli_veri_cek(hisse):
    tip, analiz_kodu = hisse_kodu_hazirla(hisse)

    try:
        df = yf.download(tickers=analiz_kodu, period="3mo", interval="1d", progress=False)
        if df.empty: return None
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # Hisseler için teknik indikatör matrisi
        df['RSI'] = df.ta.rsi(length=14)
        df['ATR'] = df.ta.atr(length=14)
        bb = df.ta.bbands(length=20, std=2)
        if bb is not None:
            df['BB_Ust'] = bb.iloc[:, 2]
            df['BB_Alt'] = bb.iloc[:, 0]
        else:
            df['BB_Ust'] = df['Close']
            df['BB_Alt'] = df['Close']
        macd = df.ta.macd()
        df['MACD'] = macd.iloc[:, 0] if macd is not None else 0
        df['MACD_Signal'] = macd.iloc[:, 2] if macd is not None else 0
        df['Hacim_MA10'] = df['Volume'].rolling(window=10).mean()
        df['Goreceli_Hacim'] = df['Volume'] / np.where(df['Hacim_MA10'] == 0, 1, df['Hacim_MA10'])
        df.dropna(inplace=True)
            
        return df
    except Exception as e:
        print(f"Derin Matris Çekim Hatası: {e}")
        return None

def yapay_zeka_ile_yorumla(hisse, analiz_tipi, veri_metni):
    if analiz_tipi == "TEKNIK":
        sistem_mesaji = (
            f"Sen Salvador Yazılım tarafından kodlanmış, net, sert ve tamamen sonuç odaklı çalışan kurumsal bir Quant Trading Analistisin. "
            f"Sana {hisse} hissesinin teknik metriklerini veriyorum. Yatırım tavsiyesi uyarısı gibi sıkıcı yasal metinleri ASLA kullanmadan, "
            f"halkın çok rahat anlayacağı dille şu sorulara NET ve kesin yanıtlar ver:\n"
            f"1) Batar mı Çıkar mı? (Hissede yön neresi, düşüş mü yükseliş mi baskın?)\n"
            f"2) Ortalama kaç günde hangi fiyata gelir? (Net bir zaman aralığı ve hedef fiyat tahmini ver)\n"
            f"3) Kısa vadeli al-sat fırsatı mı sunuyor yoksa uzun vadeli kumbara yatırımı mı?\n"
            f"4) Güvenli alım noktası neresidir ve işler ters giderse nereden kaçılmalıdır (Stop-Loss)?\n"
            f"Madde madde, kararlı ve kendinden emin yaz."
        )
    else:
        sistem_mesaji = (
            f"Sen Salvador Yazılım'ın kurumsal haber analiz motorusun. Sana {hisse} hissesiyle ilgili son güncel haber başlıklarını veriyorum.\n\n"
            f"Senden isteğim, kullanıcının hangi haberin ne anlama geldiğini net görebilmesi için ŞU FORMATTA bir rapor üretmektir:\n"
            f"1) Önce gelen haber başlıklarını aynen yaz.\n"
            f"2) Her haber başlığının hemen altına '💡 Salvador'un Çıkarımı:' başlığı açarak, o haberin halk diliyle ne anlama geldiğini, şirkete para mı sokacağını yoksa panik satışı mı getireceğini 1-2 cümleyle açıkla.\n"
            f"3) En alta da '🎯 Özet Karar' başlığıyla kısa vadede bu haberlerin hisseyi yukarı patlatıp patlatmayacağını net şekilde yaz.\n\n"
            f"Yatırım tavsiyesi uyarısı gibi sıkıcı yasal metinleri ASLA kullanma. Kararlı, net ve jargonsuz ol."
        )

    try:
        cevap = ai_model.generate_content(f"{sistem_mesaji}\n\nVERİLER:\n{veri_metni}")
        return cevap.text.strip()
    except Exception as e:
        return f"⚠️ Yapay Zeka Motoru Bağlantı Hatası: {e}"

# ==========================================
# 🚀 ANA TELEGRAM DÖNGÜSÜ
# ==========================================

def canli_tarayici_botu_calistir():
    son_guncelleme_id = 0
    print("🚀 Salvador V1.3 (Safkan Hisse Senedi Sürümü) Yayında! Portlar dinleniyor...")

    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?timeout=100&offset={son_guncelleme_id}"
            response = requests.get(url, timeout=110)
            if response.status_code != 200:
                time.sleep(2)
                continue
                
            veriler = response.json()
            if not veriler.get("ok") or not veriler.get("result"):
                time.sleep(1)
                continue
                
            for guncelleme in veriler["result"]:
                son_guncelleme_id = guncelleme["update_id"] + 1
                
                islem_listesi = []
                if "message" in guncelleme and "text" in guncelleme["message"]:
                    user_id = str(guncelleme["message"]["chat"]["id"])
                    text = guncelleme["message"]["text"].strip()
                    islem_listesi.append({"tip": "mesaj", "user_id": user_id, "veri": text})
                elif "callback_query" in guncelleme:
                    user_id = str(guncelleme["callback_query"]["message"]["chat"]["id"])
                    data = guncelleme["callback_query"]["data"]
                    islem_listesi.append({"tip": "buton", "user_id": user_id, "veri": data})
                    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery?callback_query_id={guncelleme['callback_query']['id']}")

                for islem in islem_listesi:
                    user_id = islem["user_id"]
                    
                    if islem["tip"] == "mesaj":
                        parcalar = islem["veri"].split()
                        komut = parcalar[0].upper()
                        
                        if komut == "/START":
                            karsilama = (
                                "🦅 *SALVADOR YAZILIM FİNANSAL ZEKA MERKEZİ* V1.3\n"
                                "──────────────────────────────────────\n"
                                "Selam! Ben Salvador. BIST ve ABD hisse senetlerinin anlık nabzını tutan, yapay zeka tabanlı kurumsal bir finans asistanıyım.\n\n"
                                "⚙️ *NELER YAPABİLİRİM?*\n"
                                "🔹 *Anlık Hisse Takibi:* Canlı fiyatları ve gün içindeki ucuzluk/pahalılık oranını ASCII termometresiyle ölçerim.\n"
                                "🔹 *Derin Teknik Tahmin:* RSI, MACD ve hacim matrislerini okuyarak yapay zekayla 'Batar mı, çıkar mı? Kaç günde kaça gider?' sorularına yanıt veririm.\n"
                                "🔹 *Haber Röntgeni:* Google News üzerinden en taze kurumsal gelişmeleri toplar, hisseye etkisini yorumlarım.\n"
                                "🔹 *Güvenli İşlem:* Yetkili kullanıcılardan gelen emirleri anında Alpaca üzerinden New York borsasına iletirim.\n\n"
                                "✍️ *NASIL KULLANILIR?*\n"
                                "👉 `/analiz HISSE_KODU`\n\n"
                                "📈 *Örnek Hisseler:* `/analiz TOASO`  │  `/analiz THYAO` │  `/analiz AAPL`\n"
                                "──────────────────────────────────────\n"
                                "🤖 *Salvador Emrinizde, sorgulamaya başlamak için komut gönderin!*"
                            )
                            telegram_mesaj_gonder(user_id, karsilama)

                        elif len(parcalar) > 1 and komut in ["/ANALIZ", "/ANALİZ"]:
                            girdi = parcalar[1].upper()
                            telegram_mesaj_gonder(user_id, f"⏳ *{girdi}* için Salvador derin tarama motoru başlatıldı...")
                            
                            tip, analiz_kodu = hisse_kodu_hazirla(girdi)
                            
                            try:
                                df = yf.download(tickers=analiz_kodu, period="7d", interval="1d", progress=False)
                                if isinstance(df.columns, pd.MultiIndex):
                                    df.columns = df.columns.get_level_values(0)
                                    
                                if not df.empty:
                                    canli_fiyat = float(df['Close'].values[-1])
                                    gunun_dibi = float(df['Low'].values[-1])
                                    gunun_tepesi = float(df['High'].values[-1])
                                    
                                    para_birimi = "$" if tip == "US" else "₺"
                                    
                                    fmt = ".2f"
                                    fiyat_str = f"{canli_fiyat:{fmt}}"
                                    dip_str = f"{gunun_dibi:{fmt}}"
                                    tepe_str = f"{gunun_tepesi:{fmt}}"
                                    
                                    fark = gunun_tepesi - gunun_dibi
                                    if fark > 0:
                                        komum_yuzdesi = ((canli_fiyat - gunun_dibi) / fark) * 100
                                        bar_uzunlugu = 10
                                        dolu_kisim = max(0, min(bar_uzunlugu, int((komum_yuzdesi / 100) * bar_uzunlugu)))
                                        bar = "━" * dolu_kisim + "🟢" + "━" * (bar_uzunlugu - dolu_kisim)
                                        
                                        dibe_uzaklik = ((canli_fiyat - gunun_dibi) / gunun_dibi) * 100
                                        tepeye_uzaklik = ((gunun_tepesi - canli_fiyat) / canli_fiyat) * 100
                                        
                                        if komum_yuzdesi >= 85: durum_yorumu = "⚠️ Hisse bugün gördüğü en yüksek fiyatlara çok yakın. Zirvelerde geziyor, kâr satışlarına dikkat edin."
                                        elif komum_yuzdesi <= 15: durum_yorumu = "🔥 Hisse bugün gördüğü en ucuz fiyatlara inmiş durumda. Buralardan ucuz bulup alanlar çıkabilir (Tepki ihtimali)."
                                        else: durum_yorumu = "⚖️ Fiyat günün dengeli bölgesinde. Alıcılar bir adım önde görünüyor."
                                        
                                        detay_metni = (
                                            f"📍 *Gün İçindeki Yeri:* `[{bar}]`\n"
                                            f"🔻 *En Ucuzuna Uzaklık:* %{dibe_uzaklik:.1f}\n"
                                            f"🚀 *En Pahalısına Uzaklık:* %{tepeye_uzaklik:.1f}\n\n"
                                            f"💡 *Salvador Diyor ki:* _{durum_yorumu}_"
                                        )
                                    else:
                                        detay_metni = "📍 *Durum:* Fiyat yatayda sabitlendi (İşlem görmüyor veya hafta sonu verisi)."

                                    pano = (
                                        f"⚙️ *SALVADOR {girdi} KONTROL PANELI* (Hisse Senedi)\n"
                                        f"───────────────────────\n"
                                        f"💵 *Güncel Fiyat:* {para_birimi}{fiyat_str}\n\n"
                                        f"📊 *FİYAT ARALIĞI (Son İşlem Günü)*\n"
                                        f"📉 *En Ucuz:* {para_birimi}{dip_str}  │  📈 *En Pahalı:* {para_birimi}{tepe_str}\n\n"
                                        f"{detay_metni}\n"
                                        f"───────────────────────\n"
                                        f"🤖 Salvador Yapay Zeka Modülünü Seçin:"
                                    )
                                    
                                    butonlar = [
                                        [{"text": "📰 Haberleri ve Şirketi Yorumla", "callback_data": f"HABER_{girdi}"}],
                                        [{"text": "🧠 Teknik Tahmin (Kaça Gider? Batar Mı?)", "callback_data": f"TEKNIK_{girdi}"}],
                                        [{"text": f"🛒 {girdi} OTOMATİK İŞLEM AÇ", "callback_data": f"AL_{girdi}"}]
                                    ]
                                    telegram_mesaj_gonder(user_id, pano, butonlar)
                                else:
                                    telegram_mesaj_gonder(user_id, f"❌ *Kod Bulunamadı:* {girdi} koduna ait bir hisse senedi tespit edilemedi.")
                            except Exception as e:
                                print("Enstrüman Analiz Hatası:", e)
                                telegram_mesaj_gonder(user_id, "⚠️ Panel hazırlanırken teknik bir sorun yaşandı.")
                                
                    elif islem["tip"] == "buton":
                        if "_" in islem["veri"]:
                            aksiyon, hisse = islem["veri"].split("_")[0], islem["veri"].split("_")[1]
                            
                            if aksiyon == "HABER":
                                telegram_mesaj_gonder(user_id, f"⏳ {hisse} haber havuzu ve kurumsal gelişmeler taranıyor...")
                                piyasa_verisi = pazar_gunu_guvenli_veri_cekici(hisse)
                                
                                haberler = piyasa_verisi["haberler_ham"] if (piyasa_verisi and "haberler_ham" in piyasa_verisi) else "Haber bulunamadı, şirketin genel finansal duruşu yorumlanacak."
                                
                                llm_yorumu = yapay_zeka_ile_yorumla(hisse, "HABER", haberler)
                                telegram_mesaj_gonder(user_id, f"📰 *{hisse} ŞİRKET DURUM RAPORU*\n───────────────────────\n{llm_yorumu}")
                                
                            elif aksiyon == "TEKNIK":
                                telegram_mesaj_gonder(user_id, f"⚙️ {hisse} grafikleri yapay zekaya aktarılıyor, hedefler hesaplanıyor...")
                                df_teknik = detayli_veri_cek(hisse)
                                piyasa_verisi = pazar_gunu_guvenli_veri_cekici(hisse)
                                
                                if df_teknik is not None and piyasa_verisi:
                                    son_veri = df_teknik.iloc[-1]
                                    anlik_fiyat = piyasa_verisi["fiyat"]
                                    tip, _ = hisse_kodu_hazirla(hisse)
                                    pb = "TL" if tip == "BIST" else "USD"
                                    
                                    ham_teknik = (
                                        f"Hisse: {hisse}\nCanlı Fiyat: {anlik_fiyat} {pb}\nRSI: {son_veri['RSI']:.2f}\n"
                                        f"MACD: MACD={son_veri['MACD']:.2f}, Sinyal={son_veri['MACD_Signal']:.2f}\n"
                                        f"Göreceli Hacim: {son_veri['Goreceli_Hacim']:.2f}x\n"
                                        f"Bollinger: Alt={son_veri['BB_Alt']:.2f}, Üst={son_veri['BB_Ust']:.2f}\n"
                                        f"ATR: {son_veri['ATR']:.2f}"
                                    )
                                    llm_yorumu = yapay_zeka_ile_yorumla(hisse, "TEKNIK", ham_teknik)
                                    telegram_mesaj_gonder(user_id, f"📊 *{hisse} TAHMİN & AKSİYON RAPORU*\n───────────────────────\n{llm_yorumu}")
                                else:
                                    telegram_mesaj_gonder(user_id, "❌ Teknik matris analiz için yeterli hacim verisi üretemedi.")

                            elif aksiyon == "AL":
                                if user_id in IZINLI_KULLANICILAR:
                                    tip, _ = hisse_kodu_hazirla(hisse)
                                    if tip == "BIST": 
                                        telegram_mesaj_gonder(user_id, f"✔️ *BIST Simüle Portföy:* {hisse} başarıyla ortak takip listesine eklendi.")
                                    else:
                                        api.submit_order(symbol=hisse, qty=1, side='buy', type='market', time_in_force='gtc')
                                        telegram_mesaj_gonder(user_id, f"🦅 *GERÇEK EMİR İLETİLDİ:* {hisse} alım emri Alpaca üzerinden New York borsasına uçuruldu.")
                                else: 
                                    telegram_mesaj_gonder(user_id, f"❌ *Yetki Reddedildi:* Bu işlemi gerçekleştirmek için yönetici izniniz yok.")

        except requests.exceptions.ReadTimeout:
            continue
        except Exception as e:
            print("Döngü Tıkanma Hatası:", e)
            time.sleep(2)

if __name__ == "__main__":
    canli_tarayici_botu_calistir()