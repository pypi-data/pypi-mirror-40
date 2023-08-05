def get_key_from_value(dic, value):
    values = list(dic.values())
    if value not in values:
        return None
    else:
        return list(dic.keys())[values.index(value)]
