import requests
import os
import pandas as pd  # ← テスト用にこれを追加

DATA_DIR = "data"
LATEST_XLSX = os.path.join(DATA_DIR, "latest.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)

url = "https://www.fsa.go.jp/menkyo/menkyoj/shikin_idou.xlsx"
r = requests.get(url)
r.raise_for_status()

with open(LATEST_XLSX, "wb") as f:
    f.write(r.content)

# ===== ここからテスト用コード =====
# せっかく保存したファイルを、わざと全然違う内容で上書きします
df_test = pd.DataFrame({"テスト": ["通知テストです", "データが変わりました"]})
df_test.to_excel(LATEST_XLSX, index=False)
# ===============================

print("Excel saved (with test data)")

