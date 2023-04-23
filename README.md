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
    
    Linux:
    ```
    python3 -m pip install urllib3
    ```
    Windows CMD/PowerShell:
    ```
    python -m pip install urllib3
    ```
4. Run the script and Update the record

    Windows:
      ```
      python /path/to/ddns_cloudflare.py [CF_TOKEN] [domain.com] [host.domain.com]
      ```

    Linux:
      ```
      python3 /path/to/ddns_cloudflare.py [CF_TOKEN] [domain.com] [host.domain.com]
      ```
      
5. Set a schedule to run script automaticly (Optional)

    Windows:
      - Win+R and run `taskschd.msc`
      - Set a Task with the GUI
    
    Linux:
      - Run `crontab -e` and set a cron job

        ```
        # Check and Update every 5 minutes

        */5 * * * *  /usr/bin/python3 /path/to/ddns_cloudflare.py [CF_TOKEN] [domain.com] [host.domain.com]
        ```

## Supported Platform
- Linux
  - With Python 3.6 or later
  - Tested on Ubuntu 22.04.2 LTS with Python 3.10.6
- Windows
  - With Python 3.6 or later
  - If you have AdGuard running, turn off the `DNS Protection`, otherwise the script can't get your ip.
  - Tested on Windows 11 22H2 with Python 3.9.7