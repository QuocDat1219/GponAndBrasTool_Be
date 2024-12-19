from pydantic import BaseModel, Field

class HistoryGpon(BaseModel):
    use_time: str
    user_gpon: str
    gpon_type: str
    ip_gpon: str
    feature_gpon: str
    status: str = Field(default="H")