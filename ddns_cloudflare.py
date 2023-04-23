import sys, platform, subprocess, urllib3, json

def get_current_ip():
    ip, result, platform_name = "", "", platform.system()

    if platform_name == "Linux":
        result = subprocess.run(["dig", "+short" , "txt", "chaos", "whoami.cloudflare", "@1.1.1.1"], stdout=subprocess.PIPE).stdout.decode("utf-8")
        ip = result.strip().replace('"', '')
    elif platform_name == "Windows":
        result = subprocess.run(["nslookup", "-type=TXT", "-class=CHAOS", "whoami.cloudflare", "1.1.1.1"], stdout=subprocess.PIPE).stdout.decode("utf-8")
        try:
            ip = result.split("text =")[1].strip().replace('"', '')
        except IndexError:
            print("[Error] Get IP Failure >>", result)
            exit(1)
    else:
        print("[Error]", platform_name, "is not supported.")
        exit(1)

    if len(ip) == 0:
        print("[Error] Get IP Failure >>", result)
        exit(1)

    return ip

def get_hostname_zone_id():
    r = http.request("GET", "https://api.cloudflare.com/client/v4/zones",
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + CF_TOKEN
            }
        )

    j = json.loads(r.data.decode("utf-8"))
    for i in j["result"]:
        if i["name"] == DOMAIN:
            return i["id"]
    print("[Error] Domain is not found >> " + DOMAIN) 
    exit(1)

def get_host_id_by_zone(zone_id, ip):
    r = http.request("GET", "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records".format(zone_id = zone_id),
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + CF_TOKEN
            }
        )

    j = json.loads(r.data.decode("utf-8"))
    for i in j["result"]:
        if i["name"] == HOSTNAME:
            if i["content"] == ip:
                print("[INFO] IP was up to date >> " + HOSTNAME + " | " + ip) 
                exit(0)
            return i["id"]
    print("[Error] Host is not found >> " + HOSTNAME) 
    exit(1)

def update_record(zone_id, host_id, ip):
    r = http.request("PUT", "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{host_id}".format(zone_id = zone_id, host_id = host_id),
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + CF_TOKEN
            },
            body = json.dumps({
                "content": ip,
                "name": HOSTNAME,
                "proxied": False,
                "type": "A",
                "ttl": 60
                })
        )

    j = json.loads(r.data.decode("utf-8"))
    if j["success"]:
        print("[INFO] IP updated >> " + HOSTNAME + " | " + ip) 
    else:
        print("[Error] Update Failure >>", j)

def main():
    global http, CF_TOKEN, DOMAIN, HOSTNAME
    if len(sys.argv) != 4:
        print("Usage: python3 ddns_cloudflare.py [CF_TOKEN] [DOMAIN.com] [HOST.DOMAIN.com]")
        exit(1)

    http = urllib3.PoolManager()

    CF_TOKEN = sys.argv[1]
    DOMAIN = sys.argv[2]
    HOSTNAME = sys.argv[3]

    CURR_IP = get_current_ip()
    ZONE_ID = get_hostname_zone_id()
    HOST_ID = get_host_id_by_zone(ZONE_ID, CURR_IP)
    update_record(ZONE_ID, HOST_ID, CURR_IP)

main()
