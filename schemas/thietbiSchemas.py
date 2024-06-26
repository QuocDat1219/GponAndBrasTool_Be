from config.db import conn
from bson import ObjectId

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
    serialized_list = []
    for a in entity:
        ipaddress_id = a.get('ipaddress')
        vlanims_id = a.get('vlanims')
        vlanmytv_id = a.get('vlanmytv')
        vlannet_id = a.get('vlannet')

        serialized_dict = {
            **{i: str(a[i]) for i in a if i == '_id'},
            'ipaddress': {'number': conn.gponbrastool.ipaddress.find_one({'_id': ObjectId(ipaddress_id)})['ipaddress'] , '_id' : ipaddress_id} if ipaddress_id and conn.gponbrastool.ipaddress.find_one({'_id': ObjectId(ipaddress_id)}) else None,
            'vlanims': {'number': conn.gponbrastool.vlanims.find_one({'_id': ObjectId(vlanims_id)})['number'] , '_id' : vlanims_id} if vlanims_id and conn.gponbrastool.vlanims.find_one({'_id': ObjectId(vlanims_id)}) else None,
            'vlanmytv': {'number': conn.gponbrastool.vlanmytv.find_one({'_id': ObjectId(vlanmytv_id)})['number'] , '_id' : vlanmytv_id} if vlanmytv_id and conn.gponbrastool.vlanmytv.find_one({'_id': ObjectId(vlanmytv_id)}) else None,
            'vlannet': {'number': conn.gponbrastool.vlanNet.find_one({'_id': ObjectId(vlannet_id)})['number'] , '_id' : vlannet_id} if vlannet_id and conn.gponbrastool.vlanNet.find_one({'_id': ObjectId(vlannet_id)}) else None,
            **{i: a[i] for i in a if i not in ['_id', 'ipaddress', 'vlanims', 'vlanmytv', 'vlannet']}
        }
        serialized_list.append(serialized_dict)
    return serialized_list


