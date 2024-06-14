from fastapi import Request,HTTPException
import requests
from decouple import config
# import pandas as pd

async def call_api(username: str):
    url = config("CTS_URL") + username + config("SERVICE_TYPE")
    token = config("CTS_TOKEN")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return HTTPException(status_code = 200, detail={"msg": "success", "data":  response.json()})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail={"msg": "Đã xảy ra lỗi khi lấy dữ liệu", "error": str(e)})