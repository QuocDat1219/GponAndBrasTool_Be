from fastapi import APIRouter, HTTPException, Depends
from models.googleSheetModel import GoogleSheet
from config.db import conn
from schemas.googleSheetSchemas import serializeDict, serializeList
from bson import ObjectId
from auth.jwt_bearer import jwtBearer
from service.googleSheet import loss_optical_fiber_google_sheet

googleSheetRouter = APIRouter()

@googleSheetRouter.post('/api/sheets/update')
async def update_ton_and_lap(data: dict):
    try:
        sheetId = data["google_sheet_id"]
        return await loss_optical_fiber_google_sheet(sheetId)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail={"msg": "lỗi"})
    
# Tạo mới
@googleSheetRouter.post('/api/sheets/')
async def create_link_google_sheet(googleSheetLink:GoogleSheet):
    try:
        createdGoogleSheet = conn.gponbrastool.googlesheet.insert_one(dict(googleSheetLink))
        if createdGoogleSheet:
            return HTTPException(status_code=200, detail={ "msg" : f"success", "data": serializeList(conn.gponbrastool.googlesheet.find())})
        else:
            return HTTPException(status_code=500, detail={ "msg" : f"error"})
    except:
        return HTTPException(status_code=500,detail={ "msg" : f"error"})
    
@googleSheetRouter.get("/api/sheets/")
async def get_all_google_sheet_link():
    allGooleSheetLink = serializeList(conn.gponbrastool.googlesheet.find())
    return allGooleSheetLink

@googleSheetRouter.get("/api/sheets/{id}")
async def get_google_sheet_link(id):
    googleSheetLink = conn.gponbrastool.googlesheet.find_one({"_id": ObjectId(id)})
    if googleSheetLink:
        return serializeDict(googleSheetLink)
    else:
        return HTTPException(status_code=500,detail={ "msg" : f"Không tìm thấy dữ liệu"})

@googleSheetRouter.put("/api/sheets/{id}")
async def update_google_sheet_link(id, googleSheetLink: GoogleSheet):
    try:
        conn.gponbrastool.googlesheet.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(googleSheetLink)}
        )
        updatedGoogleSheet = conn.gponbrastool.googlesheet.find_one({"_id": ObjectId(id)})
        if updatedGoogleSheet:
            return HTTPException(status_code=200, detail={ "msg" : f"success", "data": serializeList(conn.gponbrastool.googlesheet.find())})
        else:
            return HTTPException(status_code=500,detail={ "msg" : f"error"})
    except:
        return HTTPException(status_code=500,detail={ "msg" : f"error"})
    
    
@googleSheetRouter.delete('/api/sheets/{id}')
async def delete_ip_address(id):
    try:
        deleted_id = conn.gponbrastool.googlesheet.delete_one({"_id": ObjectId(id)})
        if deleted_id.deleted_count == 1:
            return HTTPException(status_code = 200, detail={ "msg" : f"success", "data": serializeList(conn.gponbrastool.googlesheet.find())})
        else:
            return HTTPException(status_code = 500,detail={ "msg" : f"error"})
    except:
        return HTTPException(status_code = 500, detail={ "msg" : f"error"})
    
