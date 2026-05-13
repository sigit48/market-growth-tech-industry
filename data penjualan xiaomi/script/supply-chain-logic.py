import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. LOAD DATA
path = r'C:\Users\LENOVO\Documents\DATA ANALYST\data penjualan xiaomi\data\full.csv'
df_full = pd.read_csv(path)

# 2. FIX TANGGAL & STATUS
df_full['Tanggal'] = pd.to_datetime(df_full['Tanggal'], dayfirst=True, errors='coerce', format='mixed')
df_full = df_full.dropna(subset=['Tanggal'])
df_full['Status'] = 'Actual'

# Konfigurasi Lead Time
lead_time_config = {
    'Asia': {'Avg_LT': 3, 'Max_LT': 5},
    'Europe': {'Avg_LT': 7, 'Max_LT': 10},
    'Latin America': {'Avg_LT': 14, 'Max_LT': 21},
    'Middle East & Africa': {'Avg_LT': 10, 'Max_LT': 15}
}

# 3. FUNGSI FORECAST
def forecast_sales(group):
    # Mengambil nama group (Wilayah, Seri)
    wilayah_val, seri_val = group.name 
    
    # PERBAIKAN: Gunakan group_sorted (pakai underscore)
    group_sorted = group.sort_values('Tanggal')
    
    y = group_sorted['Penjualan Harian (Unit)'].values
    X = np.arange(len(y)).reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Prediksi 7 hari ke depan
    future_X = np.arange(len(y), len(y) + 7).reshape(-1, 1)
    forecast = model.predict(future_X)
    
    last_date = group_sorted['Tanggal'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)
    
    return pd.DataFrame({
        'Tanggal': future_dates,
        'Wilayah': wilayah_val,
        'Seri': seri_val,
        'Penjualan Harian (Unit)': forecast.clip(min=0),
        'Status': 'Forecast'
    })

# 4. EKSEKUSI (Pastikan group_by kolomnya sesuai)
forecast_result = df_full.groupby(['Wilayah', 'Seri']).apply(forecast_sales, include_groups=False).reset_index(drop=True)
df_final = pd.concat([df_full, forecast_result], ignore_index=True)

# 5. SUPPLY CHAIN LOGIC
stats = df_full.groupby(['Wilayah', 'Seri']).agg({
    'Penjualan Harian (Unit)': ['mean', 'max']
}).reset_index()
stats.columns = ['Wilayah', 'Seri', 'Avg_Sales', 'Max_Sales']

df_final = df_final.merge(stats, on=['Wilayah', 'Seri'], how='left')

# Mapping Lead Time
def apply_lt(row):
    config = lead_time_config.get(row['Wilayah'], {'Avg_LT': 5, 'Max_LT': 7})
    return pd.Series([config['Avg_LT'], config['Max_LT']])

df_final[['Avg_LT', 'Max_LT']] = df_final.apply(apply_lt, axis=1)

# Rumus SS & ROP
df_final['Safety_Stock'] = (df_final['Max_Sales'] * df_final['Max_LT']) - (df_final['Avg_Sales'] * df_final['Avg_LT'])
df_final['Reorder_Point'] = (df_final['Avg_Sales'] * df_final['Avg_LT']) + df_final['Safety_Stock']

# 6. EXPORT FINAL
# Ubah ke string YYYY-MM-DD agar Power BI tidak rewel
df_final['Tanggal'] = pd.to_datetime(df_final['Tanggal']).dt.strftime('%Y-%m-%d')
df_final.to_csv('predictive_logistics_data.csv', index=False)

print("--------------------------------------------------")
print("✓ BERHASIL! File 'predictive_logistics_data.csv' sudah siap.")
print("--------------------------------------------------")