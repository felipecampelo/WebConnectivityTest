from http.client import HTTPConnection
from urllib.parse import urlparse
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

# def display_check_result(result, url, error=""):
#     print(f'Os status da "{url}" é:', end =" ")
#     if result:
#         print('"Online!👍"')
#     else:
#         print(f'"Offline?" 👎 \n  Erro: "{error}"')
        
# def site_is_online(url, timeout=10):
#     """Return True if the target URL is online.

#     Raise an exception otherwise.
#     """
#     error = Exception("Deu ruim!")
#     parser = urlparse(url)
#     host = parser.netloc or parser.path.split("/")[0]
#     for port in (80, 443):
#         connection = HTTPConnection(host=host, port=port, timeout=timeout)
#         try:
#             connection.request("HEAD", "/")
#             return True
#         except Exception as e:
#             error = e
#         finally:
#             connection.close()
#     raise error