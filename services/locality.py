import requests
import json

def city(token,city):
  url = "https://gateway.cdek.ru/locality/web/locality/city/getFilterData"

  payload = {
      "filter": {
          "name": f"{city}",
          "code": None,
          "lang": "rus",
          "orderPermitType": "ALL",
          "postcode": None,
          "cityImportanceFrom": None,
          "cityImportanceTo": None
      },
      "columns": [
          "ek4code",
          "shortName",
          "districtName",
          "regionName",
          "coordinates",
          "postcodes",
          "phoneCodes",
          "status",
          "isPayLimit",
          "isCashDelivery",
          "isReverseTariff",
          "creationOrdersPermitted",
          "cityImportance"
      ],
      "sort": [],
      "offset": 0,
      "limit": 100
  }

  headers = {
      'X-Auth-Token': f'{token}',
      'Accept-Encoding': 'gzip, deflate, br, zstd',
      'X-User-Locale': 'ru_RU',
      'X-User-Lang': 'rus',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
      'Content-Type': 'application/json',
      'Cookie': 'JSESSIONID=node0khpgeih3mnrj10c84vut4uhuw159685.node0'
  }

  response = requests.post(url, headers=headers, data=json.dumps(payload))


  for item in response.json()["items"]:
      if item["shortName"] == payload["filter"]["name"]:
          uuid = item["uuid"]
          break
  else:
      uuid = None
  return uuid
