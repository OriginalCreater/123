import requests
import json

def historyData(token,id):  
  url = "https://gateway.cdek.ru/order/web/journal/history/changes/v2/getFilterData"

  payload = json.dumps({
    "fields": {
      "orderNumbers": [
        f"{id}"
      ]
    },
    "sort": [
      {
        "column": "changeDateTime",
        "direction": "DESC"
      }
    ],
    "offset": 0,
    "limit": 100,
    "columns": [
      "orderNumber",
      "changeDateTime",
      "userCity",
      "userName",
      "orderChangeAttributeName",
      "attributeValueBefore",
      "attributeValueAfter"
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

  for item in response.json()['items']:
      if item['orderChangeAttributeName'] == 'Основная услуга (тариф)' : return True
  return False

