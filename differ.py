# differ.py
import pandas as pd
import os
import sys
import shutil
import hashlib

DATA_DIR = "data"
LATEST = os.path.join(DATA_DIR, "latest.xlsx")
PREVIOUS = os.path.join(DATA_DIR, "previous.xlsx")

# =========================
# ファイル内容のハッシュ
def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

# =========================
def main():
    if not os.path.exists(LATEST):
        print("latest.xlsx が存在しません。先に scrape.py を実行してください。")
        sys.exit(1)

    os.makedirs(DATA_DIR, exist_ok=True)

    # 初回実行
    if not os.path.exists(PREVIOUS):
        print("初回実行：previous.xlsx を作成します")
        shutil.copy2(LATEST, PREVIOUS)
        sys.exit(0)

    # =====================
    # ファイル全体の差分判定（高速）
    latest_hash = file_hash(LATEST)
    previous_hash = file_hash(PREVIOUS)

    if latest_hash == previous_hash:
        print("変更なし")
        sys.exit(0)

    print("変更あり")

    # =====================
    # 中身の比較（詳細用）
    df_latest = pd.read_excel(LATEST)
    df_previous = pd.read_excel(PREVIOUS)

    # 行数差
    row_diff = len(df_latest) - len(df_previous)
    print(f"行数差分: {row_diff:+}")

    # 完全一致しない行数
    diff_rows = (
        pd.concat([df_latest, df_previous])
        .drop_duplicates(keep=False)
    )
    print(f"内容が異なる行数: {len(diff_rows)}")

    # =====================
    # previous を更新
    shutil.copy2(LATEST, PREVIOUS)

    # notify.py 用（変更あり）
    sys.exit(2)

# =========================
if __name__ == "__main__":
    main()
