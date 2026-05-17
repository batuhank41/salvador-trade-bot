import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def veri_dizileri_olustur(veri, hedefler, zaman_adimi=10):
    """Veriyi LSTM'in anlayacağı 3 Boyutlu [Örnek, Zaman Adımı, Özellik] formata çevirir"""
    X, y = [], []
    for i in range(len(veri) - zaman_adimi):
        X.append(veri[i : i + zaman_adimi])
        y.append(hedefler.iloc[i + zaman_adimi])
    return np.array(X), np.array(y)

def lstm_modeli_egit(dosya_path="piyasa_egitim_verisi.csv"):
    print("🧠 Lokal grafik veri seti yükleniyor...")
    df = pd.read_csv(dosya_path, index_col=False)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    
    ozellikler = ['Mesafe_SMA200', 'Ikili_Dip_Sinyali', 'SMA_20', 'Tillson_Al', 'ALMA_Al', 'Fisher_Al', 'Goreceli_Hacim', 'Momentum_RSI']
    
    X_ham = df[ozellikler]
    y_ham = df['Hedef']
    
    # 1. ÖLÇEKLEME (Sinir ağları büyük sayılardan hoşlanmaz, veriyi 0-1 arasına ezeriz)
    scaler = MinMaxScaler()
    X_olcekli = scaler.fit_transform(X_ham)
    
    # Ölçekleyiciyi (Scaler) canlı botta kullanmak üzere kaydediyoruz
    joblib.dump(scaler, "veri_olcekleyici.pkl")
    print("✅ Veri ölçekleyici (Scaler) 'veri_olcekleyici.pkl' olarak kaydedildi.")
    
    # 2. ZAMAN SERİSİ OLUŞTURMA (Bot son 10 saate bakarak karar verecek)
    ZAMAN_ADIMI = 10
    X_3D, y_1D = veri_dizileri_olustur(X_olcekli, y_ham, ZAMAN_ADIMI)
    
    # %80 Eğitim, %20 Test
    X_train, X_test, y_train, y_test = train_test_split(X_3D, y_1D, test_size=0.2, shuffle=False)
    
    print(f"Eğitim Seti: {X_train.shape} (Örnek Sayısı, Zaman Adımı, Özellikler)")
    
    # 3. DERİN ÖĞRENME (LSTM) MİMARİSİ KURULUMU
    model = Sequential([
        # 1. LSTM Katmanı (Hafıza)
        LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
        Dropout(0.2), # Aşırı öğrenmeyi (Ezberlemeyi) önleme
        
        # 2. LSTM Katmanı (Derin Hafıza)
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        
        # Çıkış Katmanı (0 veya 1 - Düşecek veya Yükselecek)
        Dense(units=1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    print("\n🚀 Derin Sinir Ağı Eğitimi Başlıyor (Epochs)...")
    # Modeli 10 tur boyunca eğitiyoruz
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
    
    # Test Etme
    tahmin_olasiliklari = model.predict(X_test)
    tahminler = (tahmin_olasiliklari > 0.5).astype(int).flatten()
    
    print("\n================ LSTM TEST SONUÇLARI ================")
    print(f"LSTM Sinir Ağı Başarı Oranı: %{accuracy_score(y_test, tahminler) * 100:.2f}")
    print("=====================================================")
    
    # Modeli H5 formatında kaydediyoruz (TensorFlow standartı)
    model.save("lstm_trade_bot.h5")
    print("\n✅ Derin Öğrenme Beyni 'lstm_trade_bot.h5' olarak kaydedildi.")

if __name__ == "__main__":
    lstm_modeli_egit()