import sys

from asyncore import read
from checker import site_is_online
from cli import read_user_cli_args

def main():
    user_args = read_user_cli_args()
    urls = user_args.urls
    file = user_args.file

    if urls:
        _site_check(urls)
    elif file:
        _site_check(file)
    else:
        print("Você não digitou nem a URL e nem um arquivo...")
        sys.exit(1)

def _site_check(urls):
    for url in urls:
        result = site_is_online(url.rstrip('\n'))

if __name__ == "__main__":
    main()