from flask import Flask, request, abort
import os
import json
from utils.gpt_helper import extract_fridge_info
from utils.notion_helper import save_to_notion

from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

load_dotenv()

app = Flask(__name__)

# LINE token & secret
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text
    try:
        extracted = extract_fridge_info(user_input)
        save_to_notion(extracted)
        reply = f"✅ 已紀錄：{extracted['物品名稱']}（{extracted['擁有者']}），{extracted['保存期限']} 過期"
    except Exception as e:
        reply = f"❌ 發生錯誤：{str(e)}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(debug=True)