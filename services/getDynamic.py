import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


def getDinamic(uuid : str, token : str) -> bool:
    url = "https://gateway.cdek.ru/bi-report-provider/web/contragent/getOrdersDetail"

    payload = json.dumps({
    "contragentUuid": f"{uuid}"
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
    try:
        # for order in response.json()["ordersByMonth"]:]
        if len(response.json()["ordersDetail"]) < 3:
            return True
        else:
            order = response.json()["ordersDetail"][2]["deliveryDate"]
            date = order.split("-")

            # Формируем дату с первого числа месяца
            delivery_date = datetime(int(date[0]), int(date[1]), int(date[2]))
            # Проверяем, прошло ли 6 месяцев с текущей даты
            if datetime.now() >= delivery_date + relativedelta(months=6):
                return True
            else:
                return False
    except KeyError:
        return True
    