import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from streamlit_folium import st_folium

# Load cleaned Air Quality dataset
# df = pd.read_csv('cleaned_air_quality_data.csv')
# df["datetime"] = pd.to_datetime(df["datetime"])

df_part1 = pd.read_csv('cleaned_air_quality_data_part1.csv')
df_part2 = pd.read_csv('cleaned_air_quality_data_part2.csv')
df = pd.concat([df_part1, df_part2])
df["datetime"] = pd.to_datetime(df["datetime"])

# Mengatur tema seaborn
sns.set_theme(style="dark") 

# Membuat sidebar untuk filter stasiun dan rentang waktu
st.sidebar.title("Filter Data")

stations = df['station'].unique().tolist()
selected_stations = st.sidebar.multiselect('Pilih Stasiun', stations, default=stations)

min_date = df["datetime"].min()
max_date = df["datetime"].max()

start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[(df['station'].isin(selected_stations)) & 
                (df["datetime"] >= pd.to_datetime(start_date)) & 
                (df["datetime"] <= pd.to_datetime(end_date))]

# Menghitung rata-rata harian untuk PM2.5 dan PM10
daily_pollution = filtered_df.resample('D', on="datetime").agg({
    'PM2.5': 'mean',
    'PM10': 'mean'
}).reset_index()

st.header("Pola Variasi Polusi PM2.5 dan PM10")

col1, col2 = st.columns(2)
avg_pm25 = daily_pollution['PM2.5'].mean()
avg_pm10 = daily_pollution['PM10'].mean()

with col1:
    st.metric(label="Rata-rata PM2.5", value=f"{avg_pm25:.2f} µg/m³")
with col2:
    st.metric(label="Rata-rata PM10", value=f"{avg_pm10:.2f} µg/m³")

# Membuat line plot untuk tren polusi di setiap stasiun per bulan
st.subheader("Tren Bulanan Polusi di Setiap Stasiun")

filtered_df['month'] = filtered_df['datetime'].dt.month

col1, col2 = st.columns(2)
# Plot PM2.5
with col1:
    fig_tren_pm25, ax_tren_pm25 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_df, x='month', y='PM2.5', hue='station', ci=None, ax=ax_tren_pm25)
    ax_tren_pm25.set_title('Tren PM25 Bulanan di Setiap Stasiun', fontsize=16)
    ax_tren_pm25.set_xlabel('Bulan', fontsize=12)
    ax_tren_pm25.set_ylabel('Konsentrasi PM25 (µg/m³)', fontsize=12)
    ax_tren_pm25.legend(loc='upper right', title='Stasiun')
    st.pyplot(fig_tren_pm25)

# Plot PM10
with col2:
    fig_tren_pm10, ax_tren_pm10 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_df, x='month', y='PM10', hue='station', ci=None, ax=ax_tren_pm10)
    ax_tren_pm10.set_title('Tren PM10 Bulanan di Setiap Stasiun', fontsize=16)
    ax_tren_pm10.set_xlabel('Bulan', fontsize=12)
    ax_tren_pm10.set_ylabel('Konsentrasi PM10 (µg/m³)', fontsize=12)
    ax_tren_pm10.legend(loc='upper right', title='Stasiun')
    st.pyplot(fig_tren_pm10)

# Korelasi antara PM2.5, PM10, dan Faktor Cuaca
st.subheader("Korelasi antara PM2.5, PM10, dan Faktor Cuaca")

fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
corr_matrix = filtered_df[['PM2.5', 'PM10', 'TEMP', 'DEWP', 'WSPM', 'RAIN']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax_corr)
ax_corr.set_title('Korelasi antara PM2.5, PM10, dan Faktor Cuaca', fontsize=16)
st.pyplot(fig_corr)

# Menampilkan distribusi PM2.5 dan PM10
col1, col2 = st.columns(2)
st.subheader("Distribusi PM2.5 dan PM10 di Seluruh Dataset")

fig_hist, (ax_pm25, ax_pm10) = plt.subplots(1, 2, figsize=(14, 6))

# Histogram PM2.5
with col1:
    sns.histplot(filtered_df['PM2.5'], bins=50, kde=True, color='blue', ax=ax_pm25)
    ax_pm25.set_title('Distribusi PM2.5')
    ax_pm25.set_xlabel('PM2.5 (µg/m³)')
    ax_pm25.set_ylabel('Frekuensi')

# Histogram PM10
with col2:
    sns.histplot(filtered_df['PM10'], bins=50, kde=True, color='blue', ax=ax_pm10)
    ax_pm10.set_title('Distribusi PM10')
    ax_pm10.set_xlabel('PM10 (µg/m³)')
    ax_pm10.set_ylabel('Frekuensi')

st.pyplot(fig_hist)

# Menampilkan stasiun dengan rata-rata polusi tertinggi dan terendah
st.subheader("Stasiun dengan Polutan Tertinggi dan Terendah")

station_avg = df.groupby('station')[['PM2.5', 'PM10']].mean().reset_index()

station_avg_sorted_pm25 = station_avg.sort_values(by='PM2.5', ascending=False)
station_avg_sorted_pm10 = station_avg.sort_values(by='PM10', ascending=False)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors_pm25 = ["#90CAF9"] + ["#D3D3D3"] * (len(station_avg_sorted_pm25) - 1)  
colors_pm10 = ["#90CAF9"] + ["#D3D3D3"] * (len(station_avg_sorted_pm10) - 1)  
col1, col2 = st.columns(2)

# Plot untuk PM2.5
with col1:
    sns.barplot(x="PM2.5", y="station", data=station_avg_sorted_pm25, palette=colors_pm25, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Rata-rata PM2.5 (µg/m³)", fontsize=30)
    ax[0].set_title("Stasiun dengan Rata-rata PM2.5 Tertinggi", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)

# Plot untuk PM10
with col2:
    sns.barplot(x="PM10", y="station", data=station_avg_sorted_pm10, palette=colors_pm10, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Rata-rata PM10 (µg/m³)", fontsize=30)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Stasiun dengan Rata-rata PM10 Tertinggi", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Membuat Line plot untuk tren rata-rata harian PM2.5 dan PM10 berdasarkan jam
filtered_df['hour'] = filtered_df['datetime'].dt.hour

st.subheader("Pola Polusi Berdasarkan Jam")

fig_hourly, ax_hourly = plt.subplots(figsize=(12, 6))
sns.lineplot(data=filtered_df.groupby('hour')['PM2.5'].mean().reset_index(), x='hour', y='PM2.5', color='blue', label='PM2.5', ax=ax_hourly)
sns.lineplot(data=filtered_df.groupby('hour')['PM10'].mean().reset_index(), x='hour', y='PM10', color='green', label='PM10', ax=ax_hourly)
ax_hourly.set_title('Rata-rata PM2.5 dan PM10 Berdasarkan Jam', fontsize=16)
ax_hourly.set_xlabel('Jam', fontsize=12)
ax_hourly.set_ylabel('Konsentrasi PM (µg/m³)', fontsize=12)
ax_hourly.legend(title="Polutan")
st.pyplot(fig_hourly)

# Interactive Map
st.subheader("Geolokasi Stasiun dan Polusi")
# Menambahkan koordinat untuk setiap stasiun
station_coordinates = {
    'Aotizhongxin': (41.731242, 123.456778),
    'Changping': (22.983278, 114.005929),
    'Dingling': (40.289682, 116.239599),
    'Dongsi': (39.933688, 116.434355),
    'Gucheng': (39.90745, 116.190337),
    'Guanyuan': (32.4526, 105.8179),
    'Huairou': (40.27716, 116.698821),
    'Nongzhanguan': (39.933747, 116.461806),
    'Shunyi': (40.129994, 116.657023),
    'Tiantan': (39.8825, 116.4208),
    'Wanshouxigong': (39.8801, 116.3732),
    'Wanliu': (31.274028, 121.582914)
}

station_avg['coordinates'] = station_avg['station'].map(station_coordinates)

station_avg['combined_score'] = station_avg['PM2.5'] + station_avg['PM10']

# Simpan map ke session_state jika belum ada
if 'm' not in st.session_state:
    # Membuat peta dasar menggunakan folium
    m = folium.Map(location=[39.9, 116.4], zoom_start=10)

    # Menambahkan marker untuk setiap stasiun
    for _, row in station_avg.iterrows():
        if row['combined_score'] > 175:
            icon_color = 'red'
            icon = folium.Icon(color=icon_color)
        else:
            icon_color = 'green'
            icon = folium.Icon(color=icon_color)
        
        folium.Marker(
            location=row['coordinates'],
            popup=f"Stasiun: {row['station']}<br>PM2.5: {row['PM2.5']:.2f} µg/m³<br>PM10: {row['PM10']:.2f} µg/m³",
            icon=icon
        ).add_to(m)
    
    # Simpan peta ke session state
    st.session_state['m'] = m

# Tampilkan peta dalam Streamlit
st_data = st_folium(st.session_state['m'], width=700, height=500)
