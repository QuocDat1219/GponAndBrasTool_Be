from pydantic import BaseModel

class Card(BaseModel):
    number: int