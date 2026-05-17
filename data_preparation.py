import yfinance as yf
import pandas as pd
import numpy as np
import ta

def tillson_t3(close, volume_factor=0.7, period=5):
    ema1 = close.ewm(span=period, adjust=False).mean()
    ema2 = ema1.ewm(span=period, adjust=False).mean()
    ema3 = ema2.ewm(span=period, adjust=False).mean()
    ema4 = ema3.ewm(span=period, adjust=False).mean()
    ema5 = ema4.ewm(span=period, adjust=False).mean()
    ema6 = ema5.ewm(span=period, adjust=False).mean()
    c1 = -volume_factor**3
    c2 = 3*volume_factor**2 + 3*volume_factor**3
    c3 = -6*volume_factor**2 - 3*volume_factor - 3*volume_factor**3
    c4 = 1 + 3*volume_factor + 3*volume_factor**3 + 3*volume_factor**2
    return c1*ema6 + c2*ema5 + c3*ema4 + c4*ema3

def alma(close, period=9, sigma=6, offset=0.85):
    m = offset * (period - 1)
    s = period / sigma
    w = np.exp(-((np.arange(period) - m) ** 2) / (2 * (s ** 2)))
    w /= w.sum()
    return close.rolling(window=period).apply(lambda x: np.dot(x, w), raw=True)

def fisher_transform(df, period=9):
    low_min = df['Low'].rolling(window=period).min()
    high_max = df['High'].rolling(window=period).max()
    hl_range = high_max - low_min
    hl_range = np.where(hl_range == 0, 0.001, hl_range)
    value = 0.33 * 2 * ((df['Close'] - low_min) / hl_range - 0.5)
    value = np.clip(value, -0.999, 0.999)
    return 0.5 * np.log((1 + value) / (1 - value))

def piyasayi_tara_ve_hazirla():
    # 14 Hisselik Kurumsal Dev Takip Listesi
    hisse_listesi = [
        "AAPL", "NVDA", "TSLA", "MSFT", "AMD", "GOOGL", "AMZN",
        "META", "NFLX", "INTC", "AVGO", "QCOM", "BRK-B", "JPM"
    ]
    tum_veriler = []
    
    print(f"🌍 14 Hisselik Büyük Piyasa Taraması Başlatıldı:\n{hisse_listesi}\n")
    
    for hisse in hisse_listesi:
        print(f"[{hisse}] için 3 farklı stratejinin grafik verileri çıkartılıyor...")
        df = yf.download(tickers=hisse, period="2y", interval="1h", progress=False)
        if df.empty: continue
        df.columns = df.columns.get_level_values(0)
        
        # Strateji 1
        df['SMA_200'] = ta.trend.sma_indicator(close=df['Close'], window=200)
        df['Mesafe_SMA200'] = (df['Close'] - df['SMA_200']) / df['SMA_200']
        df['SMA_20'] = ta.trend.sma_indicator(close=df['Close'], window=20)
        df['Lokal_Min'] = df['Low'].rolling(window=20, center=True).min()
        df['Ikili_Dip_Sinyali'] = np.where((df['Low'] <= df['Lokal_Min'] * 1.01) & (df['Low'] >= df['Lokal_Min'] * 0.99), 1, 0)
        
        # Strateji 2
        df['Tillson_T3'] = tillson_t3(df['Close'])
        df['ALMA'] = alma(df['Close'])
        df['Fisher'] = fisher_transform(df)
        df['Tillson_Al'] = np.where(df['Close'] > df['Tillson_T3'], 1, 0)
        df['ALMA_Al'] = np.where(df['Close'] > df['ALMA'], 1, 0)
        df['Fisher_Al'] = np.where(df['Fisher'] > df['Fisher'].shift(1), 1, 0)
        
        # Strateji 3
        df['Hacim_MA10'] = df['Volume'].rolling(window=10).mean()
        df['Goreceli_Hacim'] = df['Volume'] / np.where(df['Hacim_MA10'] == 0, 1, df['Hacim_MA10'])
        df['Momentum_RSI'] = ta.momentum.rsi(close=df['Close'], window=14)
        
        # Hedef
        df['Gelecek_Kapanis'] = df['Close'].shift(-1)
        df['Hedef'] = np.where(df['Gelecek_Kapanis'] > df['Close'], 1, 0)
        
        df.dropna(inplace=True)
        tum_veriler.append(df)
        
    global_df = pd.concat(tum_veriler)
    global_df.to_csv("piyasa_egitim_verisi.csv", index=False)
    print(f"\n✅ BAŞARILI: 14 hissenin verileri birleştirildi. Toplam {len(global_df)} satır 'piyasa_egitim_verisi.csv' olarak kaydedildi!")

if __name__ == "__main__":
    piyasayi_tara_ve_hazirla()