from pydantic import BaseModel

class GoogleSheet(BaseModel):
    name: str
    link: str