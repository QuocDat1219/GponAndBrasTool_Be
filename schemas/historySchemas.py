def historyEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "use_time": item['use_time'],
        "user_gpon": item['user_gpon'],
        "gpon_type": item['gpon_type'],
        "ip_gpon": item['ip_gpon'],
        "feature_gpon": item['feature_gpon'],
        "status": item['status']
    }
    
def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]