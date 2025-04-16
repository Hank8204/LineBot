import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_fridge_info(text):
    today = datetime.today().strftime("%Y-%m-%d")
    system_prompt = (
        "你是一個冰箱共享記錄助理，請從自然語言中解析出以下欄位："
        "物品名稱、擁有者、放入日期（預設今天）、保存期限（解析成 YYYY-MM-DD）。"
        f"回傳 JSON 格式，今天是：{today}"
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