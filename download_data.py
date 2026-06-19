import os
import requests

taxi_url = os.getenv("DATA_URL")
zone_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

if not taxi_url:
    raise ValueError("DATA_URL belum tersedia. Masukkan DATA_URL lewat environment variable.")
    
files = {
"data/yellow_tripdata_2026-01.parquet": taxi_url,
"data/taxi_zone_lookup.csv": zone_url,
}

os.makedirs("data", exist_ok=True)

for file_path, url in files.items():
    print(f"Downloading {file_path}...")

    response = requests.get(url)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)

    print(f"Saved to {file_path}")


print("Download selesai.")
