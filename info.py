import socket
import ipaddress
import json

def obtener_info_ip(ip):
    resultado = {}
    try:
        ip_obj = ipaddress.ip_address(ip)
        resultado['ip'] = str(ip_obj)
        resultado['version'] = f"IPv{ip_obj.version}"
        resultado['is_private'] = ip_obj.is_private
        resultado['is_global'] = ip_obj.is_global
        resultado['is_loopback'] = ip_obj.is_loopback

        try:
            host = socket.gethostbyaddr(ip)
            resultado['host'] = {
                'name': host[0],
                'aliases': host[1]
            }
        except socket.herror:
            resultado['host'] = 'No se encontró nombre de host para la IP.'

    except ValueError as e:
        resultado['error'] = str(e)
    
    return resultado

def obtener_info_dominio(dominio):
    resultado = {}
    try:
        ip = socket.gethostbyname(dominio)
        resultado['ip'] = ip

        info = socket.gethostbyname_ex(dominio)
        resultado['canonical_name'] = info[0]
        resultado['aliases'] = info[1]
        resultado['associated_ips'] = info[2]

        info_detallada = []
        for entrada in socket.getaddrinfo(dominio, None):
            info_detallada.append({
                'family': entrada[0],
                'socket_type': entrada[1],
                'protocol': entrada[2],
                'address': entrada[4]
            })
        resultado['detailed_info'] = info_detallada

    except socket.gaierror as e:
        resultado['error'] = str(e)
    
    return resultado

# Ejemplos de uso
# info_ip = obtener_info_ip('8.8.8.8')
# info_dominio = obtener_info_dominio('google.com')
# 
# print(json.dumps({"ip_info": info_ip, "domain_info": info_dominio}, indent=4, ensure_ascii=False))

info_ip = obtener_info_ip('9.9.9.9')
info_dominio = obtener_info_dominio('www.google.com')

print(json.dumps({"ip_info": info_ip, "domain_info": info_dominio}, indent=4, ensure_ascii=False))