import websocket
import json
import time
import requests
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 从环境变量中读取配置
GOTIFY_PROTOCAL = 'wss://' if os.getenv("GOTIFY_PROTOCAL") == 'HTTPS' else 'ws://'
GOTIFY_URL = GOTIFY_PROTOCAL + os.getenv("GOTIFY_URL") + '/stream'
GOTIFY_CLIENT_TOKEN = os.getenv("GOTIFY_CLIENT_TOKEN")
PUSHDEER_URL = os.getenv("PUSHDEER_URL")
PUSHDEER_KEY = os.getenv("PUSHDEER_KEY")

def on_message(ws, message):
    """处理从 Gotify 收到的消息"""
    try:
        data = json.loads(message)
        title = data.get("title", "No Title")
        message_text = data.get("message", "No Message")
        print(f"New message received: {title} - {message_text}")
        send_to_pushdeer(title, message_text)
    except Exception as e:
        print(f"Failed to parse message: {e}")

def on_error(ws, error):
    """处理 WebSocket 错误"""
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    """处理 WebSocket 关闭"""
    print("WebSocket connection closed.")
    print(f"Close status code: {close_status_code}, Close message: {close_msg}")
    print("Reconnecting in 10 seconds...")
    time.sleep(10)
    connect_to_gotify()  # 重新连接

def on_open(ws):
    """WebSocket 连接成功"""
    print("Connected to Gotify WebSocket stream.")

def connect_to_gotify():
    """连接到 Gotify 的 WebSocket 流"""
    headers = {
        "X-Gotify-Key": GOTIFY_CLIENT_TOKEN
    }
    ws = websocket.WebSocketApp(
        GOTIFY_URL,
        header=headers,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()

def send_to_pushdeer(title, message):
    """将消息转发至 PushDeer"""
    data = {
        "pushkey": PUSHDEER_KEY,
        "text": message,
        "type": "text",
        "desp": title
    }
    response = requests.post(PUSHDEER_URL, data=data)
    if response.status_code == 200:
        print("Message sent to PushDeer successfully")
    else:
        print(f"Failed to send message to PushDeer: {response.status_code}")
        print(f"Response: {response.text}")

def main():
    """主函数，连接 Gotify 并监听消息"""
    while True:
        try:
            connect_to_gotify()
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()