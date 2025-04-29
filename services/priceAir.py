import requests
import json

def priceAir(token,fromCityUuid,toCityUuid,date):
    url = "https://gateway.cdek.ru/partnership-price-tariff/web/v1/transport/tariffs"

    payload = json.dumps({
    "sort": [],
    "offset": 0,
    "limit": 100,
    "fields": [
        {
        "field": "fromCityUuid",
        "value": None,
        "values": [
            f"{fromCityUuid}"
        ]
        },
        {
        "field": "toCityUuid",
        "value": None,
        "values": [
            f"{toCityUuid}"
        ]
        },
        {
        "field": "transportKindCode",
        "value": None,
        "values": [
            "AVIATION"
        ]
        },
        {
        "field": "startDate",
        "value": f"{date}",
        "values": None
        }
    ],
    "columns": [
        "operationType",
        "ruleGroup",
        "executorOffice",
        "executorOfficeGroup",
        "fromCountry",
        "fromCity",
        "fromOffice",
        "toCountry",
        "toCity",
        "toOffice",
        "transportKind",
        "carrier",
        "tariffMethod",
        "service",
        "serviceGroup",
        "price",
        "activeFrom",
        "activeTo"
    ]
    })
    headers = {
    'X-Auth-Token': f'{token}',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'X-User-Locale': 'ru_RU',
    'X-User-Lang': 'rus',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['items']
