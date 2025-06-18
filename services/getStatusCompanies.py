import requests
import json
import datetime
from dateutil.relativedelta import relativedelta

def get_number_affel(id : str, token : str) -> list :
    url = "https://gateway.cdek.ru/contragent/web/contragent/getOne"

    payload = json.dumps({
    "filter": {
        "uuid": f"{id}"
    }
    })
    headers = {
    'X-Auth-Token': f'{token}',
    'Origin': 'https://contragentng.cdek.ru',
    'Referer': 'https://contragentng.cdek.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    numbers = response.json()['phonesForPrintInDocument']
    if numbers != []:
        code = numbers[0]["phoneCode"]
        num = numbers[0]["number"]
        number = f"{str(code)}{str(num)}"
        return number
    else:
        return None

def get_mail_affel(id : str, token : str) -> list :
    url = "https://gateway.cdek.ru/contragent/web/contragent/getOne"

    payload = json.dumps({
    "filter": {
        "uuid": f"{id}"
    }
    })
    headers = {
    'X-Auth-Token': f'{token}',
    'Origin': 'https://contragentng.cdek.ru',
    'Referer': 'https://contragentng.cdek.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.json()['emails'] == []:
        return None
    else:
        mail = response.json()['email']
    if mail != []:
    #     code = mail[0]["phoneCode"]
    #     num = mail[0]["number"]
    #     number = f"{str(code)}{str(num)}"
        return mail
    else:
        return None

def get_name_affel(id : str, token : str) -> list :
    url = "https://gateway.cdek.ru/contragent/web/contragent/getOne"

    payload = json.dumps({
    "filter": {
        "uuid": f"{id}"
    }
    })
    headers = {
    'X-Auth-Token': f'{token}',
    'Origin': 'https://contragentng.cdek.ru',
    'Referer': 'https://contragentng.cdek.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.json()['contacts'] == []:
        return None
    else:
        contacts = response.json()['contacts']
        name = contacts[0]["name"]
        list_name = name.split(" ")
        if len(list_name) >= 3:
            return name
        else:
            return None
    #     name = response.json()['contacts']
    #     name = name["name"]
    # if name != []:
    #     code = mail[0]["phoneCode"]
    #     num = mail[0]["number"]
    #     number = f"{str(code)}{str(num)}"

    #     return contacts
def get_site_affel(id : str, token : str) -> list :
    url = "https://gateway.cdek.ru/contragent/web/contragent/getOne"

    payload = json.dumps({
    "filter": {
        "uuid": f"{id}"
    }
    })
    headers = {
    'X-Auth-Token': f'{token}',
    'Origin': 'https://contragentng.cdek.ru',
    'Referer': 'https://contragentng.cdek.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.json()['site'] == "":
        return None
    else:
        site = response.json()['site']
        return site
    # if site != []:
    # #     code = mail[0]["phoneCode"]
    # #     num = mail[0]["number"]
    # #     number = f"{str(code)}{str(num)}"
    #
    # else:
    #     return None
def getStatusCompanies(id : str, token : str) -> list :
    url = "https://gateway.cdek.ru/contragent/web/contragent/getOne"

    payload = json.dumps({
    "filter": {
        "uuid": f"{id}"
    }
    })
    headers = {
    'X-Auth-Token': f'{token}',
    'Origin': 'https://contragentng.cdek.ru',
    'Referer': 'https://contragentng.cdek.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    status = response.json()["contracts"]
    """ЕСЛИ договор отсутствует возвращаем None"""
    if response.json()["contracts"] == []:
        status = None
        signingDate = None
    else:
        """Если договор есть получаем статус"""
        status = response.json()["contracts"][0]["contractStatusCode"]
        try:
            """Если у догвора есть дата возвращает дату"""
            signingDate = response.json()["contracts"][0]["signingDate"]
        except KeyError:
            """Если у договора даты нет возвращаем None"""
            signingDate = None
    return [status, signingDate]




def checkStatusCompanies(array) -> bool:
    if array[0] == None :
        """Если договора нет возвращаем true"""
        return True
    elif (array[0] == "5" and
          datetime.datetime.now() <= datetime.datetime.strptime(array[1], '%d.%m.%Y') + relativedelta(months=6)):
        """Если договор подписан и младше 6 месяцев, возвращаем false"""
        return False
    else:
        """Если статус договора отличный от подписан возвращаем true"""
        return True
# if array[0] == '1' or array[0] == '2':
    #     return False
    #