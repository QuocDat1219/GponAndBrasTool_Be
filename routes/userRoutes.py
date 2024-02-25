from fastapi import APIRouter, Request
from models.userModel import User
from config.db import conn
from schemas.userSchemas import serializeDict, serializeList, usersEntity
from bson import ObjectId
user = APIRouter()


# getAll
@user.get('/')
async def get_all_users(request: Request):
    # client_ip = request.client.host
    # print(client_ip)
    return serializeList(conn.demo.user.find())

# getById


# @user.get('/{id}')
# async def getUserById(id):
#     print(id)
#     return serializeDict(conn.demo.user.find_one({"_id": ObjectId(id)}))

# create


@user.post('/')
async def create_user(user: User,request: Request):
    client_ip = request.client.host
    print(client_ip)
    conn.demo.user.insert_one(dict(user))
    return usersEntity(conn.demo.user.find())


@user.put('/{id}')
async def update_user(id, user: User):
    print(id)
    print(user)
    conn.demo.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    return serializeDict(conn.demo.user.find_one({"_id": ObjectId(id)}))


@user.delete('/{id}')
async def delete_user(id):
    deleted_user = conn.demo.user.find_one_and_delete({"_id": ObjectId(id)})
    if deleted_user:
        return {"message": "User deleted Successfully!"}
    else:
        return {"message": "User not found!"}
