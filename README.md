# 🦅 Salvador Finansal Zeka Merkezi (V1.3 - Safkan Hisse Senedi Sürümü)

Salvador, hem **BIST (İstanbul Borsası)** hem de **US (Amerika Borsaları)** hisse senetlerinin anlık nabzını tutan, teknik göstergeler ile piyasa haberlerini harmanlayıp yorumlayan yapay zeka tabanlı, kurumsal bir Quant Trading ve finans asistanıdır.

Salvador Yazılım çatısı altında geliştirilen bu proje; sıradan, yuvarlak cümleler kuran finans botlarının aksine, doğrudan sonuç odaklı analizler, net fiyat hedefleri ve kurumsal tüyolar üretmek üzere optimize edilmiştir.

---

## ⚙️ Çekirdek Yetenekler

* **Anlık Hisse Röntgeni (BIST & US):** Yahoo Finance API entegrasyonuyla hisselerin canlı fiyatını çeker ve özel ASCII Termometresi ile gün içindeki ucuzluk/pahalılık oranını görselleştirir.
* **Derin Teknik Matris:** Hisselerin `RSI`, `MACD`, `Bollinger Bands` ve `ATR` (Oynaklık) verilerini eş zamanlı hesaplar.
* **Google News RSS Scraper:** Şirketlerin en taze kurumsal gelişmelerini tarar, her haber başlığının altına yapay zekayla jargonsuz "Salvador'un Çıkarımı" raporunu ekler.
* **Gemini 1.5 Flash Entegrasyonu:** Matematiksel teknik matrisi ve haber havuzunu tek potada eriterek; *"Batar mı, çıkar mı? Kaç günde hangi fiyata gelir?"* sorularına kesin ve jargonsuz yanıtlar verir.
* **Güvenli Alpaca API İşlemleri:** `IZINLI_KULLANICILAR` filtresi sayesinde yetkisiz istekleri engeller. ABD borsaları için Alpaca üzerinden New York'a anlık gerçek emir fırlatır, BIST için simüle portföy işletir.

---

## 🚀 Kurulum ve Dağıtım (Deployment)

### 1. Gereksinimler
Sistem, sunucu düzeyinde izole bir sanal ortamda (`venv`) ve Python 3.12+ üzerinde çalışmaktadır. Gerekli kütüphaneler:
```bash
pip install numpy==1.26.4 pandas pandas_ta yfinance alpaca-trade-api google-generativeai beautifulsoup4 numba
