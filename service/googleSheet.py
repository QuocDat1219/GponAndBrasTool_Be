import os
import pandas as pd
import google.auth.exceptions 
import asyncio

from fastapi import HTTPException, APIRouter, Request
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_credentials():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(GoogleRequest())
            except google.auth.exceptions.RefreshError:
                # Token bị hết hạn hoặc thu hồi, xóa tệp token.json và tạo lại token mới
                os.remove("token.json")
                return get_credentials()
        else:
            flow = InstalledAppFlow.from_client_secrets_file("vnptsheetapp.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    return credentials

async def get_data_frames(service, sheet_names, sheet_id):
    data_frames = {}
    for sheet_name in sheet_names:
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=f"{sheet_name}!A1:AG").execute()
        values = result.get("values", [])
        
        if not values or len(values) <= 1:
            print(f"Sheet {sheet_name} không có dữ liệu.")
            continue
        
        header = values[0]
        data = values[1:]  # Bắt đầu từ hàng 2 để tránh hàng tiêu đề
        
        for row in data:
            if len(row) < len(header):
                row.extend([''] * (len(header) - len(row)))
            elif len(row) > len(header):
                row = row[:len(header)]
        
        df = pd.DataFrame(data, columns=header)
        df = df.dropna(how='all')
        
        data_frames[sheet_name] = df
    
    return data_frames

async def clear_and_update_sheet(service, data_list, sheet_name, sheet_id):
    try:
        # Lấy danh sách các sheet hiện có trong spreadsheet
        sheet_metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])
        
        # Kiểm tra xem sheet có tồn tại không
        sheet_exists = any(sheet.get("properties", {}).get("title") == sheet_name for sheet in sheets)
        
        if sheet_exists:
            # Xóa dữ liệu trong sheet nếu sheet tồn tại
            service.spreadsheets().values().clear(spreadsheetId=sheet_id, range=f"{sheet_name}!A1:AG1000").execute()
        else:
            # Tạo sheet mới nếu sheet không tồn tại
            requests = [{
                "addSheet": {
                    "properties": {
                        "title": sheet_name,
                        "gridProperties": {
                            "rowCount": 1000,
                            "columnCount": 34
                        }
                    }
                }
            }]
            body = {
                "requests": requests
            }
            service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=body).execute()
        
        # Ghi dữ liệu mới vào sheet
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id, 
            range=f"{sheet_name}!A1", 
            valueInputOption="RAW", 
            body={"values": data_list}
        ).execute()
    except HttpError as clear_error:
        print(f"Không thể xóa hoặc ghi dữ liệu vào sheet {sheet_name}: {clear_error}")

async def process_and_write_ton(service, data_frames, sheet_names, sheet_id):
    ton_list = [["Thiết bị", "Cổng", "Mã module quang OLT", "Mã module quang ONU", "Account Fiber",
                 "Account MyTV", "Mã nhân viên", "Thông tin nhân viên", "Độ dài", "Ngưỡng OLT Rx max",
                 "Ngưỡng OLT Rx min", "Ngưỡng OLT Tx max", "Ngưỡng OLT Tx min", "Ngưỡng ONU Rx max",
                 "Ngưỡng ONU Rx min", "Ngưỡng ONU Tx max", "Ngưỡng ONU Rx min", "Chỉ số OLT TX",
                 "Chỉ số OLT RX", "Chỉ số ONU TX", "Chỉ số ONU RX", "Chỉ số Suy hao down", "Chỉ số Suy hao up",
                 "Đánh giá", "Chỉ số kém", "Mô tả", "Trạng thái", "Tên thuê bao", "Địa chỉ lắp đặt",
                 "Điện thoại", "Datetime online gần nhất", "Ngày", "Số ngày", "Tồn"]]
    
    port_counter = {}
    
    for i in range(0, len(sheet_names) - 2, 3):
        day1, day2, day3 = sheet_names[i:i+3]
        if day1 not in data_frames or day2 not in data_frames or day3 not in data_frames:
            continue
        
        df1, df2, df3 = data_frames[day1], data_frames[day2], data_frames[day3]
        
        common_ports = set(df1['Cổng']).intersection(set(df2['Cổng']), set(df3['Cổng']))
        common_ports.discard('')
        
        if common_ports:
            for port in common_ports:
                port_counter[port] = port_counter.get(port, 0) + 1
                port_data = df3[df3['Cổng'] == port].values.flatten().tolist()
                port_data.extend([''] * (len(ton_list[0]) - len(port_data) - 1))
                port_data.append(f"Tồn lần {port_counter[port]}")
                ton_list.append(port_data)
    
    if 'N31' in data_frames:
        df28, df29, df30, df31 = data_frames.get('N28'), data_frames.get('N29'), data_frames.get('N30'), data_frames['N31']
        common_ports = set(df28['Cổng']).intersection(set(df29['Cổng']), set(df30['Cổng']), set(df31['Cổng']))
        common_ports.discard('')
        
        if common_ports:
            for port in common_ports:
                port_counter[port] = port_counter.get(port, 0) + 1
                port_data = df31[df31['Cổng'] == port].values.flatten().tolist()
                port_data.extend([''] * (len(ton_list[0]) - len(port_data) - 1))
                port_data.append(f"Tồn lần {port_counter[port]}")
                ton_list.append(port_data)
    
    if len(ton_list) > 1:
        await clear_and_update_sheet(service, ton_list, "Ton", sheet_id)
    else:
        print("Không có cổng tồn nào được tìm thấy.")

async def process_and_write_lap(service, data_frames, sheet_names, sheet_id):
    lap_list = [["Thiết bị", "Cổng", "Mã module quang OLT", "Mã module quang ONU", "Account Fiber",
                 "Account MyTV", "Mã nhân viên", "Thông tin nhân viên", "Độ dài", "Ngưỡng OLT Rx max",
                 "Ngưỡng OLT Rx min", "Ngưỡng OLT Tx max", "Ngưỡng OLT Tx min", "Ngưỡng ONU Rx max",
                 "Ngưỡng ONU Rx min", "Ngưỡng ONU Tx max", "Ngưỡng ONU Rx min", "Chỉ số OLT TX",
                 "Chỉ số OLT RX", "Chỉ số ONU TX", "Chỉ số ONU RX", "Chỉ số Suy hao down", "Chỉ số Suy hao up",
                 "Đánh giá", "Chỉ số kém", "Mô tả", "Trạng thái", "Tên thuê bao", "Địa chỉ lắp đặt",
                 "Điện thoại", "Datetime online gần nhất", "Ngày", "Số ngày", "Lặp"]]
    
    port_counter = {}
    
    for i in range(0, len(sheet_names) - 2, 3):
        day1, day2, day3 = sheet_names[i:i+3]
        if day1 not in data_frames or day2 not in data_frames or day3 not in data_frames:
            continue
        
        df1, df2, df3 = data_frames[day1], data_frames[day2], data_frames[day3]
        
        port_appearance = {}
        for port in df1['Cổng']:
            if port in port_appearance:
                port_appearance[port].append(day1)
            else:
                port_appearance[port] = [day1]
        
        for port in df2['Cổng']:
            if port in port_appearance:
                port_appearance[port].append(day2)
            else:
                port_appearance[port] = [day2]
                
        for port in df3['Cổng']:
            if port in port_appearance:
                port_appearance[port].append(day3)
            else:
                port_appearance[port] = [day3]
        
        for port, days in port_appearance.items():
            if len(days) == 2:
                second_day = days[1]
                port_counter[port] = port_counter.get(port, 0) + 1
                port_data = data_frames[second_day][data_frames[second_day]['Cổng'] == port].values.flatten().tolist()
                port_data.extend([''] * (len(lap_list[0]) - len(port_data) - 1))
                port_data.append(f"Lặp lần {port_counter[port]}")
                lap_list.append(port_data)
    
    if 'N31' in data_frames:
        df28, df29, df30, df31 = data_frames.get('N28'), data_frames.get('N29'), data_frames.get('N30'), data_frames['N31']
        
        port_appearance = {}
        for port in df28['Cổng']:
            if port in port_appearance:
                port_appearance[port].append('N28')
            else:
                port_appearance[port] = ['N28']
        
        for port in df29['Cổng']:
            if port in port_appearance:
                port_appearance[port].append('N29')
            else:
                port_appearance[port] = ['N29']
                
        for port in df30['Cổng']:
            if port in port_appearance:
                port_appearance[port].append('N30')
            else:
                port_appearance[port] = ['N30']
                
        for port in df31['Cổng']:
            if port in port_appearance:
                port_appearance[port].append('N31')
            else:
                port_appearance[port] = ['N31']
        
        for port, days in port_appearance.items():
            if len(days) == 2:
                second_day = days[1]
                port_counter[port] = port_counter.get(port, 0) + 1
                port_data = data_frames[second_day][data_frames[second_day]['Cổng'] == port].values.flatten().tolist()
                port_data.extend([''] * (len(lap_list[0]) - len(port_data) - 1))
                port_data.append(f"Lặp lần {port_counter[port]}")
                lap_list.append(port_data)
    
    if len(lap_list) > 1:
        await clear_and_update_sheet(service, lap_list, "Lap", sheet_id)
    else:
        print("Không có cổng lặp nào được tìm thấy.")

async def loss_optical_fiber_google_sheet(sheet_id):
    print(sheet_id)
    credentials = get_credentials()
    try:
        service = build("sheets", "v4", credentials=credentials)
        
        sheet_names = [f'N{str(i).zfill(2)}' for i in range(1, 32)]
        
        data_frames = await get_data_frames(service, sheet_names, sheet_id)
        await process_and_write_ton(service, data_frames, sheet_names, sheet_id)
        await process_and_write_lap(service, data_frames, sheet_names, sheet_id)
        
        return HTTPException(status_code = 200, detail={"msg": "Cập nhật thành công"})
                             
    except HttpError as error:
        raise HTTPException(status_code=500, detail={"msg": "Xảy ra lỗi"})