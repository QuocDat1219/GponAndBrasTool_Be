import asyncio
from fastapi import Request, HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT

security = HTTPBearer()

class jwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Token không hợp lệ hoặc đã hết hạn!")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token không hợp lệ hoặc đã hết hạn!")
            return self.get_payload(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Token không hợp lệ hoặc đã hết hạn!")
            
    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid

    def get_payload(self, jwtoken: str):
        return decodeJWT(jwtoken)

    # async def isUser(credentials: HTTPAuthorizationCredentials = Depends(security)):
    #     token = credentials.credentials
    #     payload = decodeJWT(token)
    #     if not payload or payload.get("role") != "user":
    #         raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập!")
    #     return payload
    
    # async def isAdmin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    #     token = credentials.credentials
    #     payload = decodeJWT(token)
    #     if not payload or payload.get("role") != "admin":
    #         raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập!")