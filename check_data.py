import pandas as pd

taxi_df = pd.read_parquet("data/yellow_tripdata_2026-01.parquet")
zone_df = pd.read_csv("data/taxi_zone_lookup.csv")

print("=== Taxi Data ===")
print("Data berhasil dibaca.")
print("Jumlah baris:", taxi_df.shape[0])
print("Jumlah kolom:", taxi_df.shape[1])
print("Preview data:")
print(taxi_df.head())

print("\n=== Zone Data ===")
print("Data berhasil dibaca.")
print("Jumlah baris:", zone_df.shape[0])
print("Jumlah kolom:", zone_df.shape[1])
print("Preview data:")
print(zone_df.head())
