import sys

from asyncore import read
from checker import site_is_online
from cli import display_check_result, read_user_cli_args

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
        error = ""
        try:
            result = site_is_online(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)

if __name__ == "__main__":
    main()