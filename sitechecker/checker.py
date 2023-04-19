import requests
from colorama import Fore, Back, Style

def site_is_online(url):
    
    https = 'https://'
    if url[:4] != 'http':
        url = https + url
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f'O site {url} está ' + Fore.GREEN + 'online! ✔️' + Style.RESET_ALL) 
        else:
            print(f'O site {url} está ' + Fore.RED + 'offline! ❌' + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(f'O site {url} está ' + Fore.RED + 'offline! ❌' + Style.RESET_ALL)