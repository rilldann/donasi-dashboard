import pandas as pd
from sqlalchemy import create_engine

# 1. Baca CSV
df = pd.read_csv("data/donasi.csv")

# 2. Koneksi ke PostgreSQL
engine = create_engine("postgresql://postgres:1@localhost:5432/visualisasi_db")

# 3. Import ke tabel donasi
df.to_sql("donasi", engine, if_exists="append", index=False)

print("Data berhasil diimport ke PostgreSQL!")
