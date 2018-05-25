def is_private_ip(client_ip):

    if client_ip is None:
        return False

    privateIPNum = {
        'A_ClassStart' :  167772160,
        'A_ClassEnd' : 184549375,
        'B_ClassStart' : 2886729728,
        'B_ClassEnd' : 2887778303,
        'C_ClassStart' : 3232235520,
        'C_ClassEnd' : 3232301055,
    }
    ip_part = client_ip.split('.')
    ipNum = int(ip_part[0])*16777216 + int(ip_part[1])*65536 + int(ip_part[2])*256 + int(ip_part[3])
    if ipNum >= privateIPNum['A_ClassStart'] and ipNum <= privateIPNum['A_ClassEnd']:
        return True
    elif ipNum >= privateIPNum['B_ClassStart'] and ipNum <= privateIPNum['B_ClassEnd']:
        return True
    elif ipNum >= privateIPNum['C_ClassStart'] and ipNum <= privateIPNum['C_ClassEnd']:
        return True

    return False
