# notify.py
import os
import subprocess
import requests

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
        result = subprocess.run(
            ["python", "differ.py"],
            capture_output=True,
            text=True
        )

        if result.returncode == 2:
            send_line("【金融庁】登録情報に変更がありました\n\n" + result.stdout)
            print("変更通知を送信しました")
        else:
            print("変更なし")

    except Exception as e:
        send_line(f"【エラー】notify.py 実行時に問題が発生しました\n{e}")
        raise


