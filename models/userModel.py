from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    fullname : str
    email: EmailStr
    password : str  
    role: str = Field(default="user")