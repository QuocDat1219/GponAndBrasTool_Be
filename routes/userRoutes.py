from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query
from models.userModel import User
from config.db import conn
from schemas.userSchemas import serializeDict, serializeList
from bson import ObjectId
from auth.jwt_handler import signJWT
from passlib.context import CryptContext
from pydantic import BaseModel
from auth.jwt_bearer import jwtBearer
userRoutes = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Login model
class LoginModel(BaseModel):
    username: str
    password: str

# Model cho đổi mật khẩu
class ChangePasswordModel(BaseModel):
    old_password: str
    new_password: str
    
# Hash password function
def hash_password(password:str) -> str:
    return pwd_context.hash(password)

# Verify password function
def verify_password(plain_password:str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#Lấy danh sách tài khoản
@userRoutes.get("/api/user/")
def get_all_user():
    try:
        # Tìm tất cả người dùng không phải là admin và không lấy trường mật khẩu
        user_list = list(conn.gponbrastool.user.find(
            {"role": {"$ne": "admin"}},  # Lọc các tài khoản không phải là admin
            {"password": 0}  # Không lấy trường mật khẩu
        ))

        if not user_list:
            return []

        return serializeList(user_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Lấy danh sách tài khoản
@userRoutes.get("/api/user/{id}")
def get_all_user(id):
    try:
        user = conn.gponbrastool.user.find_one({"_id": ObjectId(id)})
        print(user)
        if not user:
            return []
        return serializeDict(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create new user
@userRoutes.post("/api/user/")
def create_New_User(user: User):
    try:
        if conn.gponbrastool.user.find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail={"msg": "Username đã được sử dụng"})
        
        # Mã hóa password
        hashed_password = hash_password(user.password)
        user.password = hashed_password

        # Thêm trường created_at
        user_dict = dict(user)
        user_dict["created_at"] = datetime.utcnow()

        created_user = conn.gponbrastool.user.insert_one(user_dict)
        if created_user:
            return serializeDict(conn.gponbrastool.user.find_one({"_id": created_user.inserted_id}))
    except Exception as e:
        raise HTTPException(status_code=500, detail={"msg": "Không thể tạo người dùng mới", "error": str(e)})
    
    # Đăng nhập người dùng
@userRoutes.post("/api/user/login")
def login_user(user: LoginModel):
    try:
        # Tìm người dùng theo username
        db_user = conn.gponbrastool.user.find_one({"username": user.username})
        role =  db_user["role"]
        if not db_user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")
        
        # Kiểm tra mật khẩu
        if not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Sai mật khẩu")
        
        # Tạo JWT token
        token = signJWT(str(db_user["_id"]), db_user["fullname"], db_user["role"], db_user["username"])
        return {"access_token": token.get("access_token"), "role": role}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"msg": "Sai tên tài khoản hoặc mật khẩu", "error": str(e)})
    
# Đổi mật khẩu
@userRoutes.put("/api/user/change-password", dependencies=[Depends(jwtBearer())])
async def change_password(change_password_model: ChangePasswordModel, token: str = Depends(jwtBearer())):
    user_id = token["user_id"]
    if not token:
        raise HTTPException(status_code=403, detail="Token không hợp lệ hoặc đã hết hạn!")
    
    db_user = conn.gponbrastool.user.find_one({"_id": ObjectId(user_id)})
    if not db_user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")
    
    if not verify_password(change_password_model.old_password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Mật khẩu cũ không đúng")
    
    new_hashed_password = hash_password(change_password_model.new_password)
    conn.gponbrastool.user.update_one({"_id": ObjectId(user_id)}, {"$set": {"password": new_hashed_password}})
    
    return HTTPException(status_code=200,detail={"msg": "Đổi mật khẩu thành công"})

#Thay đổi quyền người dùng
# Model để thay đổi quyền
class ChangeRoleModel(BaseModel):
    role: str

# API để thay đổi quyền người dùng
@userRoutes.put("/api/user/change-role/{user_id}", dependencies=[Depends(jwtBearer())])
async def change_user_role(user_id: str, change_role_model: ChangeRoleModel, token: str = Depends(jwtBearer())):
    try:
        # Kiểm tra quyền hiện tại của người dùng
        if token["role"] != "admin":
            raise HTTPException(status_code=403, detail="Bạn không có quyền thay đổi quyền của người dùng khác")
        
        # Tìm người dùng theo user_id
        db_user = conn.gponbrastool.user.find_one({"_id": ObjectId(user_id)})
        if not db_user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")

        # Chỉ cho phép thay đổi thành các quyền hợp lệ
        valid_roles = ["admin", "user bras", "user gpon"]
        if change_role_model.role not in valid_roles:
            raise HTTPException(status_code=400, detail="Quyền không hợp lệ")
        
        # Cập nhật quyền của người dùng
        updated_role = conn.gponbrastool.user.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": change_role_model.role}})
        
        if updated_role.modified_count == 0:
            raise HTTPException(status_code = 404, detail = {"msg": "Không tìm thấy người dùng này"})
        return HTTPException(status_code=200, detail={"msg": "Thay đổi quyền thành công"})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"msg": "Không thể thay đổi quyền", "error": str(e)})
        
@userRoutes.patch("/api/user/edit/{id}")
async def edit_userInfo(id: str, fullname: str = Query(...)):
    try:
        # Cập nhật thông tin fullname cho user với id tương ứng
        updated_user = conn.gponbrastool.user.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": {"fullname": fullname}}
        )

        # Kiểm tra xem có bất kỳ tài liệu nào được cập nhật hay không
        if updated_user.modified_count == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản hoặc không có thay đổi")

        return {"msg": "Thay đổi thông tin thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"msg": "Không thể thay đổi thông tin cá nhân", "error": str(e)})