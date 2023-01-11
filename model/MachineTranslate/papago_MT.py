import os
import sys
import requests

class papago_MT:
    
    
    def __init__(self):
        self.client_id = "T5cucFxNywzZ1RT6s6lj"
        self.client_secret = "1WBZuds5yy"
        self.url = "https://openapi.naver.com/v1/papago/n2mt"
    
    def machine_translate(self, text):
        data = {'text' : text,
                'source' : 'ko',
                'target': 'en'}
        
        header = {"X-Naver-Client-Id":self.client_id,
                "X-Naver-Client-Secret":self.client_secret}

        response = requests.post(self.url, headers=header, data=data)
        rescode = response.status_code

        if(rescode==200):
            send_data = response.json()
            trans_data = (send_data['message']['result']['translatedText'])
            return send_data, trans_data
        else:
            print("Error Code:" , rescode)
            