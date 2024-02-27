from pydantic import BaseModel, validator
from ipaddress import IPv4Address
from fastapi import HTTPException

class IpAddress(BaseModel):
    ipaddress: str
    
    #Kiểm tra định dạng ip là ipV4
    @validator('ipaddress')
    def check_ip_format(cls, v):
        try:
            # Kiểm tra xem địa chỉ IP có đúng định dạng IPv4 không
            IPv4Address(v)
            return v
        except ValueError:
            # Nếu địa chỉ IP không hợp lệ, ném ra một HTTPException
            raise HTTPException(status_code=400, detail="Địa chỉ IP không hợp lệ")
