import duckdb
import pandas as pd
import requests
import numpy as np

# Binance'in bulut sunucuları (GitHub Actions vb.) için engelsiz resmi API adresi
BINANCE_API_URL = "https://data-api.binance.vision/api/v3/ticker/24hr"
FALLBACK_API_URL = "https://api.binance.com/api/v3/ticker/24hr"

def fetch_live_crypto_data():
    """Binance Canlı API'sinden 24 saatlik piyasa verilerini çeker."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(BINANCE_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        # Ana endpoint sorun çıkarırsa yedek adresi dene
        response = requests.get(FALLBACK_API_URL, headers=headers, timeout=10)
        response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)
    
    # Analiz için kritik sütunları seçiyoruz
    df = df[['symbol', 'lastPrice', 'volume', 'count', 'priceChangePercent']].copy()
    
    # Veri tiplerini dönüştürüyoruz
    df['lastPrice'] = df['lastPrice'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df['count'] = df['count'].astype(int)
    df['priceChangePercent'] = df['priceChangePercent'].astype(float)
    df['created_at'] = pd.Timestamp.now()
    
    return df

def setup_database(inject_anomaly=False):
    conn = duckdb.connect("data_observability.db")

    # 1. Canlı Binance API'den veriyi çek
    real_df = fetch_live_crypto_data()

    # 2. Geçmiş 7 günlük baseline simülasyonu
    history_data = []
    for days_back in range(7, 0, -1):
        sample_size = int(len(real_df) * np.random.uniform(0.95, 1.05))
        temp_df = real_df.sample(n=sample_size, replace=True).copy()
        temp_df['volume'] *= np.random.uniform(0.9, 1.1, size=len(temp_df))
        temp_df['created_at'] = pd.Timestamp.now() - pd.Timedelta(days=days_back)
        history_data.append(temp_df)

    df_history = pd.concat(history_data, ignore_index=True)
    conn.execute("CREATE OR REPLACE TABLE daily_transactions AS SELECT * FROM df_history")

    # 3. Bugünkü canlı veri akışı
    today_df = real_df.copy()

    # Suni anomali enjeksiyonu (Production için varsayılan False)
    if inject_anomaly:
        today_df = today_df.head(15).copy()
        today_df.loc[today_df.index % 2 == 0, 'volume'] = None

    conn.execute("CREATE OR REPLACE TABLE today_transactions AS SELECT * FROM today_df")
    return conn

if __name__ == "__main__":
    conn = setup_database(inject_anomaly=False)
    print("Binance canlı API verisi başarıyla çekildi ve DuckDB veritabanı güncellendi.")