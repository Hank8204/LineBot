import os
import requests

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_VERSION = "2022-06-28"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

def save_to_notion(data):
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "物品名稱": {
                "title": [{"text": {"content": data["物品名稱"]}}]
            },
            "擁有者": {
                "rich_text": [{"text": {"content": data["擁有者"]}}]
            },
            "放入日期": {
                "date": {"start": data["放入日期"]}
            },
            "保存期限": {
                "date": {"start": data["保存期限"]}
            }
        }
    }
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
    response.raise_for_status()