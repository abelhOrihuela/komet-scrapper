import requests
import json
import os

path = "https://api.telegram.org/bot"
token = os.getenv("API_TOKEN")


def send_item(item):
    headers = {"Content-type": "application/json"}

    response = requests.post(
        path + token + "/sendPhoto",
        data=json.dumps(
            {
                "chat_id": "-1001251894781",
                "caption": "<b>{}</b> \n {}\n <a href='{}'>Link</a>".format(
                    item["description"], item["inventory"], item["link"]
                ),
                "photo": "https:" + item["image"],
                "parse_mode": "HTML",
            }
        ),
        headers=headers,
    )

    print(response.json())
