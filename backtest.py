import pandas as pd
import numpy as np
from xgboost import XGBClassifier

def backtest_yap(veri_path="AAPL_egitim_verisi.csv", model_path="trade_bot_model.json"):
    print("Simülasyon için veriler ve yapay zeka modeli yükleniyor...")
    df = pd.read_csv(veri_path, index_col=0)
    
    # Veri temizliği (Sonsuz değerleri uçurma)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    
    # Modeli lokalden geri çağırıyoruz
    model = XGBClassifier()
    model.load_model(model_path)
    
    # [DÜZELTME]: Yapay zekanın eğitildiği 8 indikatörlük yeni geniş listeyi buraya da ekledik
    ozellikler = ['RSI', 'MACD', 'MACD_Sinyal', 'SMA_20', 'Mesafe_SMA20', 'Hacim_Degisim', 'BB_Pozisyon', 'SMA_Kesisim']
    
    # train_model.py ile senkronize olması için son %20'lik dilimi (685 satır) dinamik alıyoruz
    test_boyutu = int(len(df) * 0.2)
    test_kesiti = df.tail(test_boyutu).copy()
    
    X_test = test_kesiti[ozellikler]
    
    # Yapay zekaya tahmin yaptırıyoruz (Hata çözüldü)
    test_kesiti['Sinyal'] = model.predict(X_test)
    
    # --- SİMÜLASYON MOTORU ---
    # Hissenin saatlik gerçek getiri oranı
    test_kesiti['Hisse_Getiri'] = test_kesiti['Close'].pct_change()
    
    # Botun getirisi (Sinyal 1 ise o saatin getirisini kazanırız, 0 ise nakit)
    test_kesiti['Bot_Getiri'] = test_kesiti['Sinyal'].shift(1) * test_kesiti['Hisse_Getiri']
    
    test_kesiti.dropna(inplace=True)
    
    # Kümülatif kâr hesaplama
    kumulatif_hisse = (1 + test_kesiti['Hisse_Getiri']).cumprod() - 1
    kumulatif_bot = (1 + test_kesiti['Bot_Getiri']).cumprod() - 1
    
    print("\n================ SİMÜLASYON SONUÇLARI ================")
    print(f"Hisseyi sadece Alıp Bekleseydiniz Kâr/Zarar: %{kumulatif_hisse.iloc[-1] * 100:.2f}")
    print(f"YAPAY ZEKA BOTUNUN Toplam Kâr/Zararı:       %{kumulatif_bot.iloc[-1] * 100:.2f}")
    print("======================================================")
    
    # Grafik çizimi
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 6))
        plt.plot(kumulatif_hisse.values * 100, label="Düz Yatırım (Al ve Bekle)", color='gray', linestyle='--')
        plt.plot(kumulatif_bot.values * 100, label="Yapay Zeka Trade Botu (Gelişmiş)", color='green', linewidth=2)
        plt.title("Yapay Zeka Botu vs Düz Yatırım Performans Kıyaslaması")
        plt.xlabel("Zaman (Saat)")
        plt.ylabel("Kümülâtif Kâr/Zarar (%)")
        plt.legend()
        plt.grid(True)
        plt.savefig("trade_bot_performans.png")
        print("\nYeni performans grafiği 'trade_bot_performans.png' olarak kaydedildi.")
        plt.show()
    except Exception as e:
        print("Grafik çizdirilirken hata oluştu:", e)

if __name__ == "__main__":
    backtest_yap()