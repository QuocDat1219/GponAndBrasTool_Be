import os
import requests
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
from fastapi import HTTPException
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib.parse import urlencode

# Load các biến môi trường từ file .env
dotenv_path = Path('./env')
load_dotenv(dotenv_path=dotenv_path)

# Lấy thông tin đăng nhập từ biến môi trường
USERNAME = os.getenv('VISA_USERNAME')
PASSWORD = os.getenv('VISA_PASSWORD')

# Định nghĩa các URL cần sử dụng
SEARCH_URL = os.getenv('SEARCH_URL')
LOGIN_URL = os.getenv('LOGIN_URL')
DETAIL_URL = os.getenv('DETAIL_URL')

# Khởi tạo một session HTTP sử dụng module requests
session = requests.Session()

# Gửi yêu cầu đăng nhập và lưu lại cookies
login_data = {
    'j_username': USERNAME,
    'j_password': PASSWORD
}

async def login():
    try:
        encoded_login_data = urlencode(login_data)
        response = session.post(LOGIN_URL, data=encoded_login_data, headers={
                                'Content-Type': 'application/x-www-form-urlencoded'})
        response.raise_for_status()
        cookies = session.cookies.get_dict()
        cookies_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
        return cookies_str
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging in: {str(e)}")

async def search_user_and_get_details(username: str):
    try:
        # Đăng nhập và lấy cookies
        cookies_str = await login()

        # Chuẩn bị dữ liệu và gửi yêu cầu tìm kiếm
        search_data = {
            'bean.serviceInfo.account': username,
            'm': 'getList',
            'typeAction': 'LIST',
            'bean.organizationId': '64',
            'bean.hierarchy': 'on'
        }
        
        multipart_data = MultipartEncoder(fields=search_data)
        response_search = session.post(SEARCH_URL, data=multipart_data, headers={
            'Content-Type': multipart_data.content_type, 'Cookie': cookies_str})
        response_search.raise_for_status()

        # Phân tích kết quả tìm kiếm để lấy thông tin chi tiết
        soup = BeautifulSoup(response_search.text, 'html.parser')
        first_a_tag = soup.find('a', href=re.compile(r'bean\.id=\d+'))
        if first_a_tag:
            href = first_a_tag['href']
            bean_id = re.search(r'bean\.id=(\d+)', href).group(1)
            url_detail = f"{DETAIL_URL}{bean_id}"
            response_detail = session.get(url_detail, headers={'Cookie': cookies_str})
            response_detail.raise_for_status()

            return extract_user_details(response_detail.text)
        else:
            return HTTPException(status_code=401, detail={"msg": "Không tìm thấy tài khoản này"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def extract_user_details(html):
    soup = BeautifulSoup(html, 'html.parser')
    user_details = {}

    # Lấy các thông tin trên input
    labels = ["SYSTEMID", "SELFID", "SLOT", "PORT", "VPI"]
    # Duyệt qua các input và lấy values sau đó gắn vào obj
    for label in labels:
        input_tag = soup.find('input', {'name': re.compile(rf'serviceInfo\(.*_{label}\)')})
        if input_tag:
            user_details[label] = input_tag.get('value', '').strip()

    return HTTPException(status_code=200,detail={"msg":"success","data":user_details})