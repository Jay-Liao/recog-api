from datetime import datetime


def serialize_dict(src_obj):
    if not isinstance(src_obj, dict):
        return
    dst_obj = dict()
    for key, val in src_obj.iteritems():
        if isinstance(val, list):
            dst_obj[key] = serialize_list(val)
        elif isinstance(val, dict):
            dst_obj[key] = serialize_dict(val)
        elif isinstance(val, datetime):
            dst_obj[key] = val.isoformat()
        else:
            dst_obj[key] = val
    return dst_obj


def serialize_list(src_list):
    if not isinstance(src_list, list):
        return
    dst_list = list()
    for val in src_list:
        if isinstance(val, list):
            dst_list.append(serialize_list(val))
        elif isinstance(val, dict):
            dst_list.append(serialize_dict(val))
        elif isinstance(val, datetime):
            dst_list.append(val.isoformat())
        else:
            dst_list.append(val)
    return dst_list
