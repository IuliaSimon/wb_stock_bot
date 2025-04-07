import os
import requests
from dotenv import load_dotenv

load_dotenv()

WB_API_KEY = os.getenv("WB_API_KEY")

def get_stock_data():
    url = "https://suppliers-api.wildberries.ru/api/v3/stocks"

    headers = {
        "Authorization": WB_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        # Если это словарь с ключом 'stocks'
        if isinstance(data, dict):
            if "stocks" in data:
                stocks = data["stocks"]
                if stocks:
                    return stocks
                else:
                    return "❗️API вернул пустой список stocks"
            else:
                return f"⚠️ Ответ не содержит ключ 'stocks': {data}"
        
        # Если это список — вернём как есть
        if isinstance(data, list):
            if data:
                return data
            else:
                return "❗️API вернул пустой список"

        return f"❗️Неожиданный формат ответа от API: {type(data)}"

    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTP ошибка: {http_err}"

    except requests.exceptions.RequestException as req_err:
        return f"❌ Ошибка запроса: {req_err}"

    except Exception as err:
        return f"❌ Другая ошибка: {err}"
