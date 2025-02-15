FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# 设置默认环境变量
ENV GOTIFY_URL=yourhost.com
ENV GOTIFY_CLIENT_TOKEN=yourtoken
ENV PUSHDEER_URL=https://api2.pushdeer.com/message/push
ENV PUSHDEER_KEY=yourpushdeerkey

CMD ["python", "gotify_to_pushdeer_websocket.py"]