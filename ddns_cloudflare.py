import sys, urllib3, subprocess, json

http = urllib3.PoolManager()

def get_current_ip():
    result = subprocess.run(["dig", "+short" , "txt", "ch", "whoami.cloudflare", "@1.0.0.1"], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").replace("\n", "").replace('"', '')

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
    global CF_TOKEN, DOMAIN, HOSTNAME
    if len(sys.argv) != 4:
        print("Usage: python3 ddns_cloudflare.py [CF_TOKEN] [DOMAIN.com] [HOST.DOMAIN.com]")
        exit(1)

    CF_TOKEN = sys.argv[1]
    DOMAIN = sys.argv[2]
    HOSTNAME = sys.argv[3]

    CURR_IP = get_current_ip()
    ZONE_ID = get_hostname_zone_id()
    HOST_ID = get_host_id_by_zone(ZONE_ID, CURR_IP)
    update_record(ZONE_ID, HOST_ID, CURR_IP)

main()
