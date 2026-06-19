import os
import pandas as pd

input_file = "data/transformed/yellow_tripdata_2026-01_transformed.parquet"
output_file = "data/mart/yellow_tripdata_2026-01_cleaned.csv"

df = pd.read_parquet(input_file)

os.makedirs("data/mart", exist_ok=True)

df.to_csv(output_file, index=False)

print("Load data selesai.")
print("Hasil disimpan ke", output_file)
print("Jumlah baris:", df.shape[0])
print("Jumlah kolom:", df.shape[1])
