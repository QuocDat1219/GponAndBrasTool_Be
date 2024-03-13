from pydantic import BaseModel

class Port(BaseModel):
    port: int
    