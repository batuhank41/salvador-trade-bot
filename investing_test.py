from tradingview_ta import TA_Handler, Interval, Exchange

def tradingview_teknik_ozet_testi(hisse_sembolu):
    print(f"🕵️‍♂️ [{hisse_sembolu}] için TradingView Kurumsal Teknik Analiz motoru tetiklendi...")
    
    try:
        # TradingView analiz yöneticisini yapılandırıyoruz
        hisse = TA_Handler(
            symbol=hisse_sembolu,
            screener="america",     # Amerikan borsaları için
            exchange="NASDAQ",      # Apple, Nvidia, Tesla vb. NASDAQ üzerindedir
            interval=Interval.INTERVAL_1_HOUR # Bizim LSTM modelimiz gibi SAATLİK grafik analizi
        )
        
        # Analizi sunucudan çekiyoruz
        analiz_sonucu = hisse.get_analysis()
        
        print("\n🎯 KURUMSAL TEKNİK ÖZET SONUÇLARI:")
        print("─────────────────────────────────────────")
        # İşte o Investing'de arayıp bulamadığımız dev kurumsal karar kelimesi:
        print(f"📊 GENEL ÖZET KARARI: {analiz_sonucu.summary['RECOMMENDATION']}")
        print(f"🟢 AL Sinyali Veren İndikatör Sayısı: {analiz_sonucu.summary['BUY']}")
        print(f"⚪ NÖTR Sinyali Veren İndikatör Sayısı: {analiz_sonucu.summary['NEUTRAL']}")
        print(f"🔴 SAT Sinyali Veren İndikatör Sayısı: {analiz_sonucu.summary['SELL']}")
        
        print("\n📈 GÖSTERGE DETAYLARI (OSİLATÖRLER):")
        print("─────────────────────────────────────────")
        print(f"• Hareketli Ortalamalar Kararı: {analiz_sonucu.moving_averages['RECOMMENDATION']}")
        print(f"• Osilatörler (RSI, MACD vb.) Kararı: {analiz_sonucu.oscillators['RECOMMENDATION']}")
        
    except Exception as e:
        print(f"🚨 Kurumsal teknik motor hatası: {e}")

if __name__ == "__main__":
    # Test etmek istediğimiz hisseyi gönderiyoruz
    tradingview_teknik_ozet_testi("AAPL")