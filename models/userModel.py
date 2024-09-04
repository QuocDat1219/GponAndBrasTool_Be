from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class User(BaseModel):
    fullname: str
    username: str
    password: str  
    role: str = Field(default="user gpon")
    created_at: Optional[datetime] = None  # Optional field for created_at
