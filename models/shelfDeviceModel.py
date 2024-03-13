from pydantic import BaseModel, validator
from fastapi import HTTPException
class Shelf(BaseModel):
    number: int
