import asyncio
from fastapi import APIRouter, HTTPException, Depends
from config.db import conn
from auth.jwt_handler import signJWT
from auth.jwt_bearer import jwtBearer
from service.cts import call_api, get_user_visa

ctsRouter = APIRouter()

@ctsRouter.post("/api/cts",dependencies=[Depends(jwtBearer())])
async def get_user_cts(data: dict):
    username = data["username"]
    if username:
        return await get_user_visa(username)
    else:
        return HTTPException(status_code=500, detail={"msg":"Vui lòng nhập tài khoản người dùng"})