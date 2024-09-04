from pydantic import BaseModel, Field

class User(BaseModel):
    fullname : str
    username: str
    password : str  
    role: str = Field(default="user gpon")