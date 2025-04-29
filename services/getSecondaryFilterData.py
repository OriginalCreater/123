import requests
import json
import datetime
from dateutil.relativedelta import relativedelta


def getOMP(id : str, token : str) -> bool: 
  url = "https://gateway.cdek.ru/smr-webservice/web/smr/clientjournal/getSecondaryFilterData"

  payload = json.dumps({
    "sort": [
      {
        "field": "reportDate",
        "value": "desc"
      }
    ],
    "offset": 0,
    "limit": 50,
    "fields": [
      {
        "field": "clientUuid",
        "value": f"{id}",
        "values": None
      }
    ],
    "columns": [
      "reportType",
      "contactType",
      "reportDate",
      "clientAddress",
      "clientCityName",
      "salesManagerName",
      "contactFaceName",
      "jobPosition",
      "phoneNumbers",
      "email",
      "nextContactPurpose",
      "plannedDate",
      "notes",
      "status",
      "edit"
    ]
  })
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
  omp = response.json()['items'][:6]
  for i in response.json()['items']:
    print(i)
  data_list_omp = []

  # если нет отчёта менеджера по продажам возвращаем False
  if omp == []:
      return True
  elif omp[0]['reportType'] == "Телесейл входящий":
      return True
  else:
    last_salesManagerOffice_str = omp[0]['salesManagerName'].split('/')[1].split(',')[0]
    print(last_salesManagerOffice_str)
    # salesManagerOffice_str = salesManagerName_str.stlit('/')
    for i in omp:
        sales_ManagerOffice_str = i['salesManagerName'].split('/')[1].split(',')[0]
        if last_salesManagerOffice_str == sales_ManagerOffice_str:
            report_date_str = i["reportDate"]
            data_list_omp.append(report_date_str)
        else:
            break
    print(data_list_omp)
    report_date_str = data_list_omp[-1]
    report_date = datetime.datetime.fromisoformat(report_date_str.replace("Z", ""))
    if datetime.datetime.now() <= report_date + relativedelta(months=3):
        return False
    else:
        return True
