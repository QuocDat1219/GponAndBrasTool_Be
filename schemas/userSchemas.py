def userEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "fullname": item['fullname'],
        "username": item['username'],
        "password": item['password'],
        "role": item['role'],
    }
    
def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]