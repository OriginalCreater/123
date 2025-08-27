import time

import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


def getDoc(number: str, token: str) -> bool:
    url = "https://gateway.cdek.ru/contract/web/contract/v1/autocomplete/general/get/byFieldValue"

    payload = json.dumps({"fields": [],
                  "value": f"{number}",
                  "field": "NUMBER",
                  "limit": 10})
    headers = {
        'X-Auth-Token': f'{token}',
        'Origin': 'https://contragentng.cdek.ru',
        'Referer': 'https://contragentng.cdek.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'X-User-Lang': 'rus',
        'X-User-Locale': 'ru_RU',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    info = response.json()["items"]
    info = info[0]["uuid"]
    resauit = uuid_doc(info,token)
    print(resauit)
    time.sleep(2)
    return resauit


def uuid_doc(uuid, token):
    url = "https://gateway.cdek.ru/contract/web/contract/v2/contract/get/byUuid"

    payload = json.dumps({"uuid": f"{uuid}"})
    headers = {
        'X-Auth-Token': f'{token}',
        'Origin': 'https://contragentng.cdek.ru',
        'Referer': 'https://contragentng.cdek.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'X-User-Lang': 'rus',
        'X-User-Locale': 'ru_RU',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    g = response.json()
    g = g["billPeriodType"]["code"]
    return g
