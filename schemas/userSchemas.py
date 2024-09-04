def userEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "fullname": item['fullname'],
        "username": item['username'],
        "password": item['password'],
        "role": item['role'],
        "created_at": item.get('created_at', None)  # Include created_at field
    }
    
def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]