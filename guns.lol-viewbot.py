from concurrent.futures import ThreadPoolExecutor
import random
import colorama
import cloudscraper
import requests
import os
import sys

# Initialize colorama
colorama.init()

banner = r"""
 $$$$$$\          $$\          $$$$$$\  
$$  __$$\         \__|        $$  __$$\ 
$$ /  $$ |$$$$$$\ $$\ $$$$$$\ \__/  $$ |
\$$$$$$$ $$  __$$\$$ $$  __$$\ $$$$$$  |
 \____$$ $$ |  \__$$ $$ /  $$ $$  ____/ 
$$\   $$ $$ |     $$ $$ |  $$ $$ |      
\$$$$$$  $$ |     $$ $$$$$$$  $$$$$$$$\ 
 \______/\__|     \__$$  ____/\________|
                     $$ |               
                     $$ |               
                     \__|               
"""
print(banner)

config_file = "config.txt"

def get_username():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            content = file.read().strip()
            if content.startswith("username:"):
                return content.split(":", 1)[1].strip()
    return None

def set_username(username):
    with open(config_file, 'w') as file:
        file.write(f"username:{username}")

def restart_program():
    """Clear the Command Prompt and restart the program"""
    print("Restarting program...")
    os.system('cls')  # Clear the Command Prompt
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Check for existing username in config.txt
username = get_username()

if not username:
    print("No config found!")
    username = input("Please enter your guns.lol username: ")
    set_username(username)
    print(f"Username '{username}' has been set and saved to config.")
    restart_program()  # Restart the program after setting the username
else:
    print(f"Username found in config: {username}")

headers = {
    "accept": "*/*",
    "accept-language": "?0; Mobile",
    "cache-control": "no-cache",
    "content-length": "0",
    "origin": "https://guns.lol",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://guns.lol/" + username,
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"126.0.6478.127\"",
    "sec-ch-ua-full-version-list": "\"Not/A)Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"126.0.6478.127\", \"Google Chrome\";v=\"126.0.6478.127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"15.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "username": username
}

successful_requests = 0

# Function to get proxies using the specified ProxyScrape API
def get_proxies():
    api_url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=ipport&format=text&timeout=20000"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            return proxies
        else:
            print(f"Error: Unable to fetch proxies. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception occurred while fetching proxies: {e}")
        return []

def test(proxies):
    global username, headers, successful_requests
    while True:
        prox = random.choice(proxies)
        proxy = "http://" + prox
        proxyDict = {
            "http": proxy,
            "https": proxy
        }
        try:
            scraper = cloudscraper.create_scraper(delay=10)
            response = scraper.post("https://guns.lol/api/view/" + username, headers=headers, proxies=proxyDict)
            if response.status_code == 200:
                successful_requests += 1
                print(colorama.Fore.GREEN + f"[{successful_requests} Requests has been sent]" + colorama.Style.RESET_ALL)
        except Exception as e:
            pass

if __name__ == "__main__":
    proxies = get_proxies()
    if proxies:
        with ThreadPoolExecutor(max_workers=301) as exc:
            for i in range(300):
                exc.submit(test, proxies)
