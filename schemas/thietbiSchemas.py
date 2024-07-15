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

def serializeVlannet(entity) -> list:
    list_vlannet = []
    for a in entity:
        if isinstance(a, dict):  # Kiểm tra xem a có phải là dict không
            vlannet_id = a.get('vlannet')
            if vlannet_id:
                vlannet = conn.gponbrastool.vlanNet.find_one({'_id': ObjectId(vlannet_id)})
                if vlannet:
                    serialized_dict = {
                        "number": vlannet["number"],
                        "_id": str(vlannet["_id"])
                    }
                    list_vlannet.append(serialized_dict)
    return list_vlannet

def serializeThietBiByIp(ip_address: str) -> list:
    # Tìm ip trong collection ip
    ip_entry = conn.gponbrastool.ipaddress.find_one({"ipaddress": ip_address})
    print(ip_entry)
    if not ip_entry:
        return []

    # Tìm thiết bị dựa trên _id của ip
    thietbi_list = list(conn.gponbrastool.thietbi.find({"ipaddress": str(ip_entry["_id"])}))
    if not thietbi_list:
        return []

    # Serialize danh sách thiết bị
    serialized_list = []
    for a in thietbi_list:
        ipaddress_id = a.get('ipaddress')
        vlanims_id = a.get('vlanims')
        vlanmytv_id = a.get('vlanmytv')
        vlannet_id = a.get('vlannet')

        serialized_dict = {
            **{i: str(a[i]) for i in a if i == '_id'},
            'ipaddress': {'number': conn.gponbrastool.ipaddress.find_one({'_id': ObjectId(ipaddress_id)})['ipaddress'], '_id': ipaddress_id} if ipaddress_id and conn.gponbrastool.ipaddress.find_one({'_id': ObjectId(ipaddress_id)}) else None,
            'vlanims': {'number': conn.gponbrastool.vlanims.find_one({'_id': ObjectId(vlanims_id)})['number'], '_id': vlanims_id} if vlanims_id and conn.gponbrastool.vlanims.find_one({'_id': ObjectId(vlanims_id)}) else None,
            'vlanmytv': {'number': conn.gponbrastool.vlanmytv.find_one({'_id': ObjectId(vlanmytv_id)})['number'], '_id': vlanmytv_id} if vlanmytv_id and conn.gponbrastool.vlanmytv.find_one({'_id': ObjectId(vlanmytv_id)}) else None,
            'vlannet': {'number': conn.gponbrastool.vlanNet.find_one({'_id': ObjectId(vlannet_id)})['number'], '_id': vlannet_id} if vlannet_id and conn.gponbrastool.vlanNet.find_one({'_id': ObjectId(vlannet_id)}) else None,
            **{i: a[i] for i in a if i not in ['_id', 'ipaddress', 'vlanims', 'vlanmytv', 'vlannet']}
        }
        serialized_list.append(serialized_dict)
    return serialized_list


