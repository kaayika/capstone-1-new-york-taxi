# New York Taxi Data Pipeline
Nama : Ni Nyoman Kayika Manuhita
Kelas : Data Engineering JCDEAH-009

## Project Overview
Project ini adalah pipeline sederhana untuk memproses data perjalanan New York Taxi bulan Januari 2026.

Pipeline ini mencakup proses download data, check data, transformasi data, load data, data quality check, automation, dan Dockerization.

Alur pipeline:

```text
Download Data
→ Check Data
→ Transform Data
→ Load Data
→ Data Quality Check
→ Automation
→ Dockerization
```

## Data Source
Data yang digunakan:

1. `yellow_tripdata_2026-01.parquet`
2. `taxi_zone_lookup.csv`

Data taxi utama diambil dari environment variable `DATA_URL`.

```bash
DATA_URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet"
```

File `taxi_zone_lookup.csv` digunakan untuk mapping lokasi pickup dan dropoff berdasarkan location ID.

## Project Structure
```text
new_york_taxi/
├── data/
│   ├── yellow_tripdata_2026-01.parquet
│   ├── taxi_zone_lookup.csv
│   ├── transformed/
│   │   └── yellow_tripdata_2026-01_transformed.parquet
│   └── mart/
│       ├── yellow_tripdata_2026-01_cleaned.csv
│       ├── cleaned/
│       │   └── yellow_tripdata_2026-01_valid.csv
│       └── quarantine/
│           └── yellow_tripdata_2026-01_invalid.csv
├── logs/
│   └── pipeline.log
├── scripts/
│   └── run_pipeline.sh
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── download_data.py
├── check_data.py
├── transform_data.py
├── load_data.py
└── data_quality_check.py
```

## Requirements
Library Python yang digunakan:

```text
requests
pandas
pyarrow
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Pipeline Process
### 1. Download Data

Script: `download_data.py`

Script ini digunakan untuk mendownload data taxi dan taxi zone lookup.

Output:

```text
data/yellow_tripdata_2026-01.parquet
data/taxi_zone_lookup.csv
```

Jika file sudah tersedia di folder `data`, proses download akan dilewati agar tidak perlu download ulang.

### 2. Check Data
Script: `check_data.py`

Script ini digunakan untuk membaca data dan menampilkan informasi awal seperti jumlah baris, jumlah kolom, dan preview data.

### 3. Transform Data
Script: `transform_data.py`

Transformasi yang dilakukan:

* Standarisasi nama kolom menjadi format `snake_case`
* Konversi kolom datetime
* Membuat kolom `trip_duration_minutes`
* Membuat kolom `pickup_date`, `pickup_hour`, dan `pickup_day_name`
* Membuat kolom `is_weekend`
* Membuat kolom `time_period`
* Mapping `payment_type`
* Mapping `store_and_fwd_flag`
* Mapping lokasi pickup dan dropoff menggunakan `taxi_zone_lookup.csv`

Output:

```text
data/transformed/yellow_tripdata_2026-01_transformed.parquet
```

### 4. Load Data
Script: `load_data.py`

Script ini digunakan untuk menyimpan data hasil transformasi ke format CSV.

Output:

```text
data/mart/yellow_tripdata_2026-01_cleaned.csv
```

### 5. Data Quality Check
Script: `data_quality_check.py`

Validasi data yang dilakukan:

* Jika `trip_duration_minutes <= 0`, maka data dianggap invalid
* Jika `trip_distance <= 0`, maka data dianggap invalid

Data valid dan invalid dipisahkan ke folder berbeda.

Output data valid:

```text
data/mart/cleaned/yellow_tripdata_2026-01_valid.csv
```

Output data invalid:

```text
data/mart/quarantine/yellow_tripdata_2026-01_invalid.csv
```

## Run Pipeline Locally
Jalankan pipeline secara otomatis menggunakan shell script:

```bash
DATA_URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet" ./scripts/run_pipeline.sh
```

Log proses pipeline akan tersimpan di:

```text
logs/pipeline.log
```

## Run Pipeline with Docker
Build dan jalankan pipeline menggunakan Docker Compose:

```bash
docker compose up --build
```

Untuk menghentikan container:

```bash
docker compose down
```

Jika terjadi error saat build Docker, gunakan command berikut untuk melihat log lebih detail:

```bash
docker compose build --no-cache --progress=plain
docker compose up
```

## Final Output
Output akhir dari project ini:

```text
data/yellow_tripdata_2026-01.parquet
data/taxi_zone_lookup.csv
data/transformed/yellow_tripdata_2026-01_transformed.parquet
data/mart/yellow_tripdata_2026-01_cleaned.csv
data/mart/cleaned/yellow_tripdata_2026-01_valid.csv
data/mart/quarantine/yellow_tripdata_2026-01_invalid.csv
logs/pipeline.log
```

## Notes
File parquet tidak bisa dibuka langsung seperti file CSV biasa. File parquet dibaca menggunakan Python dengan library seperti pandas dan pyarrow.

Jika file data sudah tersedia di folder `data`, script download akan melakukan skip download agar pipeline tetap bisa berjalan tanpa perlu mendownload ulang data.
