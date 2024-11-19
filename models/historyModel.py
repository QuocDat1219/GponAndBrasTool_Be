from pydantic import BaseModel, Field

class HistoryGpon(BaseModel):
    history: str
    status: str = Field(default="H")