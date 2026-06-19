import os
import pandas as pd

input_file = "data/mart/yellow_tripdata_2026-01_cleaned.csv"

df = pd.read_csv(input_file)

os.makedirs("data/mart/cleaned", exist_ok=True)
os.makedirs("data/mart/quarantine", exist_ok=True)

df["error_type"] = ""

duration_invalid = df["trip_duration_minutes"] <= 0
distance_invalid = df["trip_distance"] <= 0

df.loc[duration_invalid, "error_type"] = "duration invalid"
df.loc[distance_invalid, "error_type"] = "distance invalid"

both_invalid = duration_invalid & distance_invalid
df.loc[both_invalid, "error_type"] = "duration invalid, distance invalid"

invalid_df = df[df["error_type"] != ""].copy()
valid_df = df[df["error_type"] == ""].copy()

valid_df = valid_df.drop(columns=["error_type"])

valid_df.to_csv(
    "data/mart/cleaned/yellow_tripdata_2026-01_valid.csv",
    index=False
)

invalid_df.to_csv(
    "data/mart/quarantine/yellow_tripdata_2026-01_invalid.csv",
    index=False
)

print("Data quality check selesai.")
print("Jumlah data valid:", valid_df.shape[0])
print("Jumlah data invalid:", invalid_df.shape[0])

print("\nJumlah error berdasarkan tipe:")
print(invalid_df["error_type"].value_counts())
