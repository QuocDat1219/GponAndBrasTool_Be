from pydantic import BaseModel

class ThietBi(BaseModel):
    loaithietbi: str
    tenthietbi: str
    ipaddress: str
    vlanims: str
    vlanmytv: str
    vlannet: str