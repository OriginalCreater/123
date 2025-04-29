import requests
import json



def get_id_affel(phone : str, token : str) -> [str] :
    url = "https://gateway.cdek.ru/contragent/web/contragent/search/byFilters"

    payload = json.dumps({
    "sort": [],
    "offset": 0,
    "limit": 100,
    "fields": [{"field": "phone", "value": f'{phone}', "values": None}],
    "columns": [
        "id",
        "countryName",
        "cityName",
        "name",
        "type",
        "inn",
        "kpp",
        "exclusiveRightOwners",
        "legalEntityDate",
        "site",
        "responsibleOfficeName",
        "note",
        "electronicDocumentManagementTypeName"
    ]
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
    inn = [item['inn'] for item in response.json()['items']]
    return inn
def get_id_companies(inn : int, token : str) -> [str] : 
    url = "https://gateway.cdek.ru/contragent/web/contragent/search/byFilters"

    payload = json.dumps({
    "sort": [],
    "offset": 0,
    "limit": 100,
    "fields": [
        {
        "field": "innFullMatch",
        "value": f"{inn}",
        "values": None
        }
    ],
    "columns": [
        "id",
        "countryName",
        "cityName",
        "name",
        "type",
        "inn",
        "kpp",
        "exclusiveRightOwners",
        "legalEntityDate",
        "site",
        "responsibleOfficeName",
        "note",
        "electronicDocumentManagementTypeName"
    ]
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
    uuids = [item['uuid'] for item in response.json()['items']]
    return uuids
