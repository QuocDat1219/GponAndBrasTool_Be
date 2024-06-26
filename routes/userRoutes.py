from fastapi import APIRouter, HTTPException, Depends
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

# Create new user
@userRoutes.post("/api/user/")
def create_New_User(user: User):
    try:
        if conn.gponbrastool.user.find_one({"username": user.username}):
            return HTTPException(status_code=400, detail={"msg": "Username đã được sử dụng"})
        
        # Mã hóa password
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        
        created_user = conn.gponbrastool.user.insert_one(dict(user))
        if created_user:
            return serializeDict(conn.gponbrastool.user.find_one({"_id": created_user.inserted_id}))
    except Exception as e:
        return HTTPException(status_code=500, detail={"msg": "Không thể tạo người dùng mới", "error": str(e)})
    
    # Đăng nhập người dùng
@userRoutes.post("/api/user/login")
def login_user(user: LoginModel):
    try:
        # Tìm người dùng theo username
        db_user = conn.gponbrastool.user.find_one({"username": user.username})
        if not db_user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")
        
        # Kiểm tra mật khẩu
        if not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Sai mật khẩu")
        
        # Tạo JWT token
        token = signJWT(str(db_user["_id"]), db_user["fullname"], db_user["role"], db_user["username"])
        return token
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