import sys, socket, platform, subprocess, urllib3, json

def get_current_ip(ipv6 : bool):
    ip, result, platform_name = "", "", platform.system()

    if not ipv6:
        if platform_name == "Linux":
            result = subprocess.run(["dig", "+short" , "txt", "chaos", "whoami.cloudflare", "@1.1.1.1"], stdout=subprocess.PIPE).stdout.decode("utf-8")
            ip = result.strip().replace('"', '')
        elif platform_name == "Windows":
            result = subprocess.run(["nslookup", "-type=TXT", "-class=CHAOS", "whoami.cloudflare", "1.1.1.1"], stdout=subprocess.PIPE).stdout.decode("utf-8")
            try:
                ip = result.split("text =")[1].strip().replace('"', '')
            except IndexError:
                print("[Error] Get IPv4 Failure >>", result)
                exit(1)
        else:
            print("[Error]", platform_name, "is not supported.")
            exit(1)
    else:
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            sock.connect(('2001:4860:4860::8888', 1))
            ip = sock.getsockname()[0]
        except:
            print("[Error] Get IPv6 Failure")
            exit(1)
        finally:
            if 'sock' in locals().keys():
                sock.close()
                
    if len(ip) == 0:
        print("[Error] Get IP" + ( "v4" if not ipv6 else "v6" ) + " Failure >>", result)
        return None

    return ip

def get_hostname_zone_id():
    r = http.request("GET", "https://api.cloudflare.com/client/v4/zones",
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + CF_TOKEN
            }
        )

    try:
        j = json.loads(r.data.decode("utf-8"))
        for i in j["result"]:
            if i["name"] == DOMAIN:
                return i["id"]
        return None
    except TypeError:
        print("[Error] API Error") 
        return None

def get_host_id_by_zone(zone_id, ip, ipv6: bool):
    r = http.request("GET", "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records".format(zone_id = zone_id),
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + CF_TOKEN
            }
        )

    try:
        j = json.loads(r.data.decode("utf-8"))
        for i in j["result"]:
            if i["name"] == HOSTNAME and i["type"] == ("A" if not ipv6 else "AAAA"):
                if i["content"] == ip:
                    print("[INFO] IP" + ( "v4" if not ipv6 else "v6" ) + " was up to date >> " + HOSTNAME + " | " + ip) 
                    return None
                return i["id"]
        print("[Error] Host is not found >> " + HOSTNAME) 
        return None
    except TypeError:
        print("[Error] API Error") 
        return None

def update_record(zone_id, host_id, ip, ipv6: bool):
    r = http.request("PUT", "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{host_id}".format(zone_id = zone_id, host_id = host_id),
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + CF_TOKEN
            },
            body = json.dumps({
                "content": ip,
                "name": HOSTNAME,
                "proxied": False,
                "type": ("A" if not ipv6 else "AAAA"),
                "ttl": 60
                })
        )

    j = json.loads(r.data.decode("utf-8"))
    if j["success"]:
        print("[INFO] IP" + ( "v4" if not ipv6 else "v6" ) + " Update Successful >> " + HOSTNAME + " | " + ip) 
    else:
        print("[Error] IP" + ( "v4" if not ipv6 else "v6" ) + " Update Failure >>", j)

def main():
    global http, CF_TOKEN, DOMAIN, HOSTNAME
    if len(sys.argv) != 5:
        print("Usage: python3 ddns_cloudflare.py [CF_TOKEN] [DOMAIN.com] [HOST.DOMAIN.com] [IPv6:true/false]")
        exit(1)

    http = urllib3.PoolManager()

    CF_TOKEN = sys.argv[1]
    DOMAIN = sys.argv[2]
    HOSTNAME = sys.argv[3]
    IPV6ENABLE = sys.argv[4].lower() == "true"

    CURR_IP = get_current_ip(False)
    if CURR_IP != None:
        ZONE_ID = get_hostname_zone_id()
        if ZONE_ID != None:
            HOST_ID = get_host_id_by_zone(ZONE_ID, CURR_IP, False)
            if HOST_ID != None:
                update_record(ZONE_ID, HOST_ID, CURR_IP, False)
    
    if not IPV6ENABLE:
        return 0
    
    CURR_IP = get_current_ip(True)
    if CURR_IP != None:
        ZONE_ID = get_hostname_zone_id()
        if ZONE_ID != None:
            HOST_ID = get_host_id_by_zone(ZONE_ID, CURR_IP, True)
            if HOST_ID != None:
                update_record(ZONE_ID, HOST_ID, CURR_IP, True)

main()
