from fastapi import APIRouter, HTTPException, Depends
from models.historyModel import HistoryGpon
from config.db import conn
from schemas.historySchemas import serializeDict, serializeList
from bson import ObjectId
from auth.jwt_bearer import jwtBearer
historyRoutes = APIRouter()

@historyRoutes.get("/api/history",dependencies=[Depends(jwtBearer())])
def get_all_history():
    try:
        histories = serializeList(conn.gponbrastool.history.find())
        if histories:
            return histories
        else:
            return []
    except Exception as e:
        return HTTPException(status_code=500, detail={"msg": "error " + str(e)})

@historyRoutes.delete("/api/history", dependencies=[Depends(jwtBearer())])
def delete_history():
    try:
        deleted_history = conn.gponbrastool.history.delete_many({"status": "H"})
        if deleted_history.deleted_count > 0:
            return HTTPException(status_code = 200, detail={ "msg" : f"success", "data": serializeList(conn.gponbrastool.history.find())})
        else:
             return HTTPException(status_code = 500,detail={ "msg" : f"error"})
    except Exception as e:
        return HTTPException(status_code=500, detail={"msg": "error " + str(e)})