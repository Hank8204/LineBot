import os
from flask import Flask, request, abort
from dotenv import load_dotenv

from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhook import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError

load_dotenv()

app = Flask(__name__)

# 初始化
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
channel_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

parser = WebhookParser(channel_secret)
messaging_api = MessagingApi(channel_token)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    for event in events:
        if event.event_type == "message":
            msg = event.message
            if msg.type == "text":
                # 你可以呼叫 ChatGPT 或 Notion 這裡
                reply_msg = f"你剛說了：{msg.text}"
                messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=reply_msg)]
                    )
                )

    return "OK"