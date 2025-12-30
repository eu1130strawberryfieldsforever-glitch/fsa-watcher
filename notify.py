import os
import subprocess
import requests
import shutil  # ファイルのコピーに必要です

LINE_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_USER_ID = os.environ["LINE_USER_ID"]

def send_line(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [
            {"type": "text", "text": message}
        ]
    }
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()

if __name__ == "__main__":
    try:
        # 1. 金融庁から最新エクセルをダウンロード
        subprocess.run(["python", "scrape.py"], check=True) 

        # 2. 前回のファイルと比較する
        result = subprocess.run(
            ["python", "differ.py"],
            capture_output=True,
            text=True
        )

        # 3. differ.py が「変更あり(2)」を返した場合のみ通知
        if result.returncode == 2:
            # LINEを送る
            send_line("【金融庁】登録情報に変更がありました\n\n" + result.stdout)
            
            # 今回の最新を「次回用の前回データ」として保存
            shutil.copy2("data/latest.xlsx", "data/previous.xlsx")
            print("変更通知を送信し、データを更新しました")
            
        else:
            print("変更なし")

    except Exception as e:
        send_line(f"【エラー】notify.py 実行時に問題が発生しました\n{e}")
        raise
