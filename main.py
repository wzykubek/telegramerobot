import requests
from os import environ
import json
from datetime import datetime
from time import sleep

TOKEN = environ.get("TOKEN")
CHANNEL_ID = "@wowneromemes"

while True:
    memes = json.loads(requests.get("https://suchwow.xyz/api/list").text)

    for meme in memes[::-1]:
        with open("db.json", "r") as f:
            db = json.loads(f.read())

        if meme["id"] in db:
            print("skip")
            continue
        else:
            date = datetime.strptime(meme["timestamp"], "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d, %H:%M:%S GMT")
            title = meme["title"]
            media = meme["image"]
            submitter = meme["submitter"]
            address = meme["address"]
            meme_url = meme["href"]

            params = {
                "chat_id": CHANNEL_ID,
                "photo": media,
                "parse_mode": "HTML",
                "caption": f'<b>{title}</b>\n\n<i>Submitted by <a href="https://suchwow.xyz/?submitter={submitter}">{submitter}</a> at {date}</i>.\n\nDonate author:\n<code>{address}</code>',
                "reply_markup": {
                    "inline_keyboard": [[{"text": "Original post", "url": meme_url}]]
                }
            }

            url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            r = requests.post(url, json=params)

            print(r.text)

            db.append(meme["id"])
            with open("db.json", "w") as f:
                f.write(json.dumps(db))

            sleep(3)

