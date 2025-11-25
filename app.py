# IMPORT SEMUA LIBRARY YANG DIBUTUHKAN
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# JUDUL DASHBOARD
st.set_page_config(
    page_title="Dashboard Donasi",
    page_icon="📊",
    layout="wide"
)
# STYLE CSS TAMBAHAN
# ============================
st.markdown("""
<style>
.big-metric {
    font-size: 32px;
    font-weight: bold;
    color: #2e6ff3;
}
.metric-label {
    font-size: 14px;
    color: #555;
}
.stProgress > div > div {
    background-color: #2e6ff3;
}
</style>
""", unsafe_allow_html=True)

# ============================
# HEADER + LOGO
# ============================
colA, colB = st.columns([2, 8])

with colA:
    st.image("images/logo.png", width=200)

with colB:
    st.markdown("""
        <div style='padding-bottom: 100px;'>
            <h1>Dashboard Donasi Kota Balikpapan</h1>
            <h3>Visualisasi Interaktif Berbasis Database PostgreSQL</h3>
        </div>
    """, unsafe_allow_html=True)

# --- 1. BACA DATA ---
# df = pd.read_csv("data/donasi.csv")

# --- BACA DATA DARI POSTGRESQL ---
engine = create_engine("postgresql://postgres:1@localhost:5432/visualisasi_db")

df = pd.read_sql("SELECT * FROM donasi", engine)

# --- 2. PREPROCESS ---
df['tanggal'] = pd.to_datetime(df['tanggal'])
df['bulan'] = df['tanggal'].dt.to_period('M').astype(str)

# Tampilkan Tabel
st.subheader("Data Donasi")
st.dataframe(df)

# --- FILTER KAMPANYE ---
st.sidebar.header("Filter Data")

kampanye_list = ['Semua'] + sorted(df['kampanye'].unique())
kampanye = st.sidebar.selectbox("Pilih Kampanye", kampanye_list)

# Data setelah filter kampanye
if kampanye == "Semua":
    filtered_df = df.copy()
else:
    filtered_df = df[df['kampanye'] == kampanye]

# --- FILTER TANGGAL ---
min_date = df['tanggal'].min().date()
max_date = df['tanggal'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date]
)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_df = filtered_df[
    (filtered_df['tanggal'] >= start_date) &
    (filtered_df['tanggal'] <= end_date)
]

# Tampilkan data setelah filter
st.subheader(f"Data Donasi — Filter Kampanye: {kampanye}")
st.dataframe(filtered_df)

# --- METRIC DASHBOARD ---
st.markdown("## 📌 Ringkasan Donasi")

total_donasi = filtered_df['jumlah'].sum()
jumlah_donatur = filtered_df['nama_donatur'].nunique()
target_donasi = 10000000  # target tahunan

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<p class='metric-label'>Total Donasi</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='big-metric'>Rp {total_donasi:,}</p>", unsafe_allow_html=True)

with col2:
    st.markdown("<p class='metric-label'>Jumlah Donatur</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='big-metric'>{jumlah_donatur}</p>", unsafe_allow_html=True)

with col3:
    st.markdown("<p class='metric-label'>Pencapaian Target</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='big-metric'>{(total_donasi / target_donasi) * 100:.2f}%</p>", unsafe_allow_html=True)

st.progress(total_donasi / target_donasi)

# --- VISUALISASI PETA LOKASI DONATUR ---
st.subheader("Peta Lokasi Donatur")

# Streamlit membutuhkan dataframe hanya dengan kolom lat dan lon
if {'lat', 'lon'}.issubset(filtered_df.columns):
    st.map(filtered_df[['lat', 'lon']].dropna())
else:
    st.warning("Kolom lat/lon tidak ditemukan pada dataset.")



# --- 3. VISUALISASI TREN DONASI PER BULAN ---
st.subheader("Tren Donasi per Bulan (Setelah Filter)")

donasi_bulanan = filtered_df.groupby('bulan')['jumlah'].sum().sort_index()

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(donasi_bulanan.index, donasi_bulanan.values, marker='o')
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Donasi (Rp)")
ax.set_title("Tren Donasi Berdasarkan Filter")
ax.grid(True)

st.pyplot(fig)


# FOOTER
st.markdown("""
<hr>
<center>
<p style='color: gray;'>
Dashboard Donasi • Dibangun menggunakan Python, Streamlit, dan PostgreSQL<br>
© 2025 Sistem Informasi — Institut Teknologi Kalimantan
</p>
</center>
""", unsafe_allow_html=True)