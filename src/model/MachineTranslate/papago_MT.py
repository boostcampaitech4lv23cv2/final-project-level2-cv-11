import os
import sys
import requests

from dotenv import load_dotenv


class Papago_MT:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("PAPAGO_ID")
        self.client_secret = os.getenv("PAPAGO_SECRET")
        self.url = "https://openapi.naver.com/v1/papago/n2mt"

    def request(self, text):
        data = {"text": text, "source": "ko", "target": "en"}

        header = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }

        response = requests.post(self.url, headers=header, data=data)
        rescode = response.status_code

        if rescode == 200:
            send_data = response.json()
            trans_data = send_data["message"]["result"]["translatedText"]
            return send_data, trans_data
        else:
            print("Error Code:", rescode)

    def machine_translate(self, merged_boxes):
        for idx, box in enumerate(merged_boxes):
            _, trans_data = self.request(box[2])
            merged_boxes[idx].append(trans_data)

        return merged_boxes
