import requests
import os

DATA_DIR = "data"
LATEST_XLSX = os.path.join(DATA_DIR, "latest.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)

url = "https://www.fsa.go.jp/menkyo/menkyoj/shikin_idou.xlsx"
r = requests.get(url)
r.raise_for_status()

with open(LATEST_XLSX, "wb") as f:
    f.write(r.content)

print("Excel saved")
