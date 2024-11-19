def historyEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "history": item['history'],
        "stats": item['status']
    }
    
def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]