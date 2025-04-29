import requests
import json
import datetime
from dateutil.relativedelta import relativedelta



def getOrderDetail(contragentUuid, token : str): 
    url = "https://gateway.cdek.ru/bi-report-provider/web/contragent/getOrdersDetail"

    payload = json.dumps({
    "limit": 100,
    "offset": 0,
    "sort": [
        {
        "field": "year",
        "value": "DESC"
        },
        {
        "field": "month",
        "value": "DESC"
        }
    ],
    "contragentUuid": f"{contragentUuid}"
    })
    headers = {
    'X-Auth-Token': f'{token}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'X-User-Locale': 'ru_RU',
    'X-User-Lang': 'rus',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    orderDetail = response.json()['ordersDetail']
    for order in orderDetail:
        date = order['deliveryDate']
        print(date)
    # если нет отчёта менеджера по продажам возвращаем False
    # if omp == []:
    #     return False
    
    # for i in omp:
    #     report_date_str = i["reportDate"]
    #     report_date = datetime.datetime.fromisoformat(report_date_str.replace("Z", ""))
    #     if datetime.datetime.now()  <=  report_date + relativedelta(months=6):
    #         return False
        
    return True

    def checkDinamic():
        pass

getOrderDetail("feb05f50-0144-446d-965a-26bbd2f99d2f","eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJleHAiOjE3NDAxMjc1NDMsImxvZ2luIjoia3JhaW5vdi5lIiwidXVpZCI6ImJmZjQ1ZTBiLWU5ZTItNGZkNC04ZTg0LTM0M2FhZDZhZjc2OCIsImRldmljZSI6IkJST1dTRVIiLCJpbmRpdmlkdWFsVXVpZCI6IjIyNmFkNzE0LWQwYzUtNDM4NC05NWViLTRiNTJkMDRmYTJhMiIsImhhc0V4Y2hhbmdlIjpmYWxzZSwiZWR1VXNlcm5hbWUiOiJvLnN0dWRlbnQ2MTgzMyIsImlzcyI6Imh0dHBzOi8vcGRwLnByb2R1Y3Rpb24uazhzLWxvY2FsLmNkZWsucnU6ODAiLCJ1c2VyIjp7ImlkIjoyNjQ4MDEsInV1aWQiOiIxZGNkNmMzOS1kYjVjLTQ3NTQtOGM3ZS1lNDJlNWU1YWQwN2YiLCJlbXBsb3llZVV1aWQiOiI3YjE4NDllMy1jNzY3LTQ3ODQtYmM5OS1iZDY2ZGFiZDA1NDkiLCJwb3NpdGlvbiI6eyJ1dWlkIjoiYTg1MWExY2QtODIwYi00MGJiLWIwNDYtYmMxYWFiZTVlYTM5IiwibmFtZSI6IiIsIm5hbWVzIjp7ImVuZyI6IlNhbGVzIE1hbmFnZXIiLCJydXMiOiLQnNC10L3QtdC00LbQtdGAINC_0L4g0L_RgNC-0LTQsNC20LDQvCJ9fSwib2ZmaWNlIjp7InV1aWQiOiJlZmM1YTM5Ny0zZWQ4LTQ4ZTktYTdjNy1mN2Q2MTc3YWY1NzMiLCJuYW1lIjoiIn19LCJ1c2VySWQiOjI2NDgwMSwidXNlclV1aWQiOiIxZGNkNmMzOS1kYjVjLTQ3NTQtOGM3ZS1lNDJlNWU1YWQwN2YiLCJlbXBsb3llZVV1aWQiOiI3YjE4NDllMy1jNzY3LTQ3ODQtYmM5OS1iZDY2ZGFiZDA1NDkiLCJwb3NpdGlvblV1aWQiOiJhODUxYTFjZC04MjBiLTQwYmItYjA0Ni1iYzFhYWJlNWVhMzkiLCJvZmZpY2VVdWlkIjoiZWZjNWEzOTctM2VkOC00OGU5LWE3YzctZjdkNjE3N2FmNTczIn0.Zf0MZhPkGIhQaFAeH5G5HIwg_v7h-OQmy6DMjFKovkipkaYskjKtzEPwU2RHqOVfdOg9w14oNons6oqnoXQuqUMvV9epKGBoeTxkUmysfm8gtujjGfxIqD2yS1COKg6ALjMpZ64a1kq-v-6tz-JWSlKZDiG7a7gdKk5cqhAzcwCXPj4sPdjrDQSvGgRb_8G1M3nioiieHD1LJ-MZxMehnxsFqHhUaxs8ShS9vg-fAhFTk-cVZ2Trs_vWc2xnpLRcMcUEj-BZEQzhRuTk0rXTwtkOmFaIzJZyHcnT0JIfgMDidRnP0jm4VF1tHM0prTcsy58KdTf1zKJBo-HmSYXs_fLpTIUaSvmTc47G_aN7rMy9OfZrlbWUwfTpKYkydAyGwPrMMptiekchKA-DkFizffVnv8xx-NaUipEp7O7bI_DLpR4PYIFViEa54pWKYqiXJ0z1umutV7yBT5bIQy9BIOV6UpbrCXOxLtCKEPSKIGaiTc16ZX_ChVLu0fH3f5IQNKtoE_rXKcFkBjsttwm2Nf-JtazN9Rb24-PkkHRrD5m4GYaelUWIGjdtMEq9gNsKeGJc_Z-L65qjA5IjyeL2torPhYHlbw6VR78ab03ejuz1dVlk9yJn0DRjkHdS87KEHkNa0C6gL0M_p5bzj8kCiAO1ApCta3owY_urgB8mq2s")