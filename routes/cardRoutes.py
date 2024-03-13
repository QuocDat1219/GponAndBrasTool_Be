from fastapi import APIRouter, HTTPException
from models.cardModel import Card
from config.db import conn
from schemas.cardSchemas import serializeDict,serializeList
from bson import ObjectId

cardRoutes = APIRouter()

@cardRoutes.post("/api/card/")
async def create_card(card: Card):
    try:
        created_card = conn.demo.card.insert_one(dict(card))
        if created_card:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")


@cardRoutes.get("/api/card/")
async def get_all_card():
    try:
        all_card = serializeList(conn.demo.card.find())
        return all_card
    except:
        return HTTPException(status_code=500, detail="error")
    
    
@cardRoutes.get("/api/card/{id}")
async def get_card_by_id(id):
    try:
        card = serializeDict(conn.demo.card.find_one({"_id": ObjectId(id)}))
        return card
    except:
        return HTTPException(status_code=500, detail="error")
        
@cardRoutes.put("/api/card/{id}")
async def update_card(id, card: Card):
    try:
        conn.demo.card.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(card)}
        )
        updated_card = serializeDict(conn.demo.card.find_one({"_id": ObjectId(id)}))
        if updated_card:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error") 

@cardRoutes.delete("/api/card/{id}")
async def delete_card(id):
    try:
        deleted_card = conn.demo.card.delete_one({"_id": ObjectId(id)})
        if deleted_card.deleted_count > 0:
           return HTTPException(status_code=200, detail="success")
        else:
           return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")