import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handle_user_message(text):
    today = datetime.today().strftime("%Y-%m-%d")
    system_prompt = (
        "你是一個 LINE Bot 助理，負責以下兩件事：\\n"
        "1. 如果使用者的語句與冰箱共享記錄有關（如：放入物品、保存期限），請解析為以下 JSON 格式：\\n"
        "{\\\"intent\\\": \\\"fridge\\\", \\\"data\\\": { \\\"物品名稱\\\": ..., \\\"擁有者\\\": ..., \\\"放入日期\\\": ..., \\\"保存期限\\\": ... }}\\n"
        f"其中放入日期預設為今天（{today}），保存期限請解析為 YYYY-MM-DD。\\n"
        "2. 若不是冰箱記錄用途，請根據使用者的提問給出回答，並包裝成如下 JSON：\\n"
        "{\\\"intent\\\": \\\"chat\\\", \\\"answer\\\": \\\"這裡放你的回答內容\\\"}\\n"
        "請務必輸出標準 JSON 格式。\\n"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)