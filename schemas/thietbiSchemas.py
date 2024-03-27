def systemEntity(item) -> dict:
    return {
        "id":str((item["_id"])),
        "loaithietbi": item["loaithietbi"],
        "tenthietbi": item["ipaddress"],
        "ipaddress": item["ipaddress"],
        "vlanims": item["vlanims"],
        "vlanmyty": item["vlanmyty"],
        "vlanet": item["vlanet"],
    }
    
    
def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]