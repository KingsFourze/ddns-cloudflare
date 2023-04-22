# DDNS-CloudFlare
A Python3 script that implements DDNS functionality through CloudFlare DNS.

## Installation
1. Clone this repo.
    ```
    git clone https://github.com/KingsFourze/ddns-cloudflare.git
    ```
2. Copy `ddns_cloudflare.py` to wherever you like.
    ```
    cd ddns-cloudflare
    cp ddns_cloudflare.py /path/to/ddns_cloudflare.py
    ```
3. Install `urllib3` package if you don't have it.

    Before installation, please make sure you have pip already installed.
   
    ```
    python3 -m pip install urllib3
    ```
4. Set cron job with `crontab -e`

    Update every 5 minutes
    
    ```
    */5 * * * *  /usr/bin/python3 /path/to/ddns_cloudflare.py [CF_TOKEN] [domain.com] [host.domain.com]
    ```
5. Save and Done.

## Supported Platform
- Linux
  - With python 3.6+

Tested on Ubuntu 22.04.2 LTS with Python 3.10.6
