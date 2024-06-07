import asyncio
from fastapi import APIRouter, HTTPException, Depends
from config.db import conn
from auth.jwt_handler import signJWT
from auth.jwt_bearer import jwtBearer
from service.visa import search_user_and_get_details
visaRoutes = APIRouter()

@visaRoutes.post("/api/visa/user/", dependencies=[Depends(jwtBearer())])
async def get_user_visa(data: dict):
    username = data["username"]
    if username:
        return await search_user_and_get_details(username)
    else:
        return HTTPException(status_code=500, detail={"msg":"Vui lòng nhập tài khoản người dùng"})