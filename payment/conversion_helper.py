import requests, json


def convert(base_currency, target_currency, amount):
    if base_currency == target_currency:
        return amount
    convert_rate_url = f"https://web-production-5516e.up.railway.app/conversion/convert/?base_currency={base_currency}&target_currency={target_currency}&amount={amount}"
    response = requests.request("GET", url=convert_rate_url, headers={})
    response_json = json.loads(response.content)
    converted_amount = response_json["converted_amount"]
    rounded_amount = round(converted_amount, 3)
    return rounded_amount


def getRate(base_currency, target_currency):
    get_rate_url = f"https://web-production-5516e.up.railway.app/conversion/getRate/?base_currency={base_currency}&target_currency={target_currency}"
    response = requests.request("GET", url=get_rate_url, headers={})
    response_json = json.loads(response.content)
    exchange_rate = response_json["exchange_rate"]
    return exchange_rate
