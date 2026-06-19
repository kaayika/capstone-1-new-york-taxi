import os
import pandas as pd

taxi_df = pd.read_parquet("data/yellow_tripdata_2026-01.parquet")
zone_df = pd.read_csv("data/taxi_zone_lookup.csv")

# =========================

# 1. Standarisasi nama kolom

# =========================

taxi_df.columns = taxi_df.columns.str.strip().str.lower().str.replace(" ", "_")

zone_df.columns = zone_df.columns.str.strip().str.lower().str.replace(" ", "_")

taxi_df = taxi_df.rename(
    columns={
        "vendorid": "vendor_id",
        "ratecodeid": "ratecode_id",
        "pulocationid": "pu_location_id",
        "dolocationid": "do_location_id",
    }
)

# =========================

# 2. Transformasi datetime

# =========================

taxi_df["tpep_pickup_datetime"] = pd.to_datetime(
    taxi_df["tpep_pickup_datetime"], errors="coerce"
)

taxi_df["tpep_dropoff_datetime"] = pd.to_datetime(
    taxi_df["tpep_dropoff_datetime"], errors="coerce"
)

taxi_df["trip_duration_minutes"] = (
    taxi_df["tpep_dropoff_datetime"] - taxi_df["tpep_pickup_datetime"]
).dt.total_seconds() / 60

taxi_df["pickup_date"] = taxi_df["tpep_pickup_datetime"].dt.date
taxi_df["pickup_hour"] = taxi_df["tpep_pickup_datetime"].dt.hour
taxi_df["pickup_day_name"] = taxi_df["tpep_pickup_datetime"].dt.day_name()
taxi_df["is_weekend"] = taxi_df["pickup_day_name"].isin(["Saturday", "Sunday"])


def categorize_time_period(hour):
    if pd.isna(hour):
        return "Unknown"
    elif 0 <= hour <= 5:
        return "Late Night"
    elif 6 <= hour <= 10:
        return "Morning"
    elif 11 <= hour <= 15:
        return "Afternoon"
    elif 16 <= hour <= 19:
        return "Evening Rush"
    elif 20 <= hour <= 23:
        return "Night"
    else:
        return "Unknown"


taxi_df["time_period"] = taxi_df["pickup_hour"].apply(categorize_time_period)

# =========================

# 3. Pastikan kolom numeric

# =========================

numeric_columns = [
    "fare_amount",
    "tip_amount",
    "total_amount",
    "extra",
    "mta_tax",
    "tolls_amount",
    "improvement_surcharge",
    "congestion_surcharge",
    "airport_fee",
    "cbd_congestion_fee",
    "trip_distance",
]

for col in numeric_columns:
    if col in taxi_df.columns:
        taxi_df[col] = pd.to_numeric(taxi_df[col], errors="coerce")

# =========================

# 4. Categorical mapping

# =========================

payment_type_mapping = {
    1: "Credit Card",
    2: "Cash",
    3: "No Charge",
    4: "Dispute",
    0: "Unknown",
}

taxi_df["payment_type_name"] = taxi_df["payment_type"].map(payment_type_mapping)
taxi_df["payment_type_name"] = taxi_df["payment_type_name"].fillna("Unknown")

store_and_fwd_mapping = {"Y": "Store and Forward", "N": "Normal"}

taxi_df["store_and_fwd_flag_name"] = taxi_df["store_and_fwd_flag"].map(
    store_and_fwd_mapping
)
taxi_df["store_and_fwd_flag_name"] = taxi_df["store_and_fwd_flag_name"].fillna(
    "Unknown"
)

# =========================

# 5. Mapping lokasi

# =========================

pickup_zone = zone_df.rename(
    columns={
        "locationid": "pu_location_id",
        "borough": "pickup_borough",
        "zone": "pickup_zone",
        "service_zone": "pickup_service_zone",
    }
)

dropoff_zone = zone_df.rename(
    columns={
        "locationid": "do_location_id",
        "borough": "dropoff_borough",
        "zone": "dropoff_zone",
        "service_zone": "dropoff_service_zone",
    }
)

taxi_df = taxi_df.merge(
    pickup_zone[
        ["pu_location_id", "pickup_borough", "pickup_zone", "pickup_service_zone"]
    ],
    on="pu_location_id",
    how="left",
)

taxi_df = taxi_df.merge(
    dropoff_zone[
        ["do_location_id", "dropoff_borough", "dropoff_zone", "dropoff_service_zone"]
    ],
    on="do_location_id",
    how="left",
)

# =========================

# 6. Simpan hasil transformasi

# =========================

os.makedirs("data/transformed", exist_ok=True)

taxi_df.to_parquet(
    "data/transformed/yellow_tripdata_2026-01_transformed.parquet", index=False
)

print("Transformasi selesai.")
print("Hasil disimpan ke data/transformed/yellow_tripdata_2026-01_transformed.parquet")
print("Jumlah baris:", taxi_df.shape[0])
print("Jumlah kolom:", taxi_df.shape[1])

print("\nPreview kolom lokasi:")
print(
    taxi_df[
        [
            "pu_location_id",
            "pickup_borough",
            "pickup_zone",
            "do_location_id",
            "dropoff_borough",
            "dropoff_zone",
        ]
    ].head()
)
