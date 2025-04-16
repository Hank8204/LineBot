import os
from flask import Flask, request, abort
from dotenv import load_dotenv

from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, TextMessage, ReplyMessageRequest
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
from utils.gpt_helper import handle_user_message
from utils.notion_helper import save_to_notion

# 載入 .env
load_dotenv()

# 初始化 Flask
app = Flask(__name__)

# LINE 設定值
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# 驗證變數是否存在
if channel_secret is None or channel_access_token is None:
    raise ValueError("請確認 LINE_CHANNEL_SECRET 與 LINE_CHANNEL_ACCESS_TOKEN 已正確設定為環境變數")

# 初始化 Webhook Parser 與 Messaging API
handler = WebhookHandler(channel_secret)
configuration = Configuration(access_token=channel_access_token)
api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)

# 預設首頁（非必要）
@app.route("/", methods=["GET"])
def index():
    return "Hello from your Line Bot v3! ✅"

# 接收 webhook 請求
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    handler.handle(body, signature)

    return "OK"

@handler.add(MessageEvent)
def handle_message(event):
    if isinstance(event.message, TextMessageContent):
        user_text = event.message.text

        try:
            result = handle_user_message(user_text)
            if result["intent"] == "fridge":
                save_to_notion(result["data"])
                reply_text = (
                    f"✅ 已紀錄：{result['data']['物品名稱']}（{result['data']['擁有者']}），"
                    f"保存至 {result['data']['保存期限']}"
                )
            elif result["intent"] == "chat":
                reply_text = result["answer"]
            else:
                reply_text = "不好意思，我不太懂你的意思，可以再說一次嗎？"

        except Exception as e:
            print("❌ 錯誤：", e)
            reply_text = f"❌ 發生錯誤：{str(e)}"

        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
