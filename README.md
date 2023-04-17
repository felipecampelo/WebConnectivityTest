# Fundamentos de Computação Tooltorial

Neste tutorial faremos uma aplicação simples em Python para validar conceitos básicos na linguagem Python e versionamento de código. Essa aplicação vai validar se um URL está online ou offline e retornar uma mensagem para o usuário.

Ao final do projeto deveremos ter a seguinte estrutura de arquivos:

```
README.md
requirements.txt
site_checker.sh
sitechecker/
├── checker.py
├── cli.py
├── __init__.py
├── __main__.py
```
# Instruções

## 1. Criar o ambiente de trabalho

Para criar um projeto python é recomendável trabalhar com ambientes virtuais, para isso você iniciar um terminal e rodar os seguintes comandos:

```
cd meuprojeto/
python -m venv venv
source venv/bin/activate
```

Se você estiver usando Windows, o comando deverá ser o seguinte>

```
PS> python -m venv venv
PS> venv\Scripts\activate
(venv) PS>
```

## 2. Criar o verificador de sites

Vamos começar criando uma simples função em Python que que verifica se um site está online usando o pacote `urllib` e`http`. Para isso podemos o código abaixo em uma sessão interativa:

```
>>> from http.client import HTTPConnection

>>> connection = HTTPSConnection("indicium.tech", port=80, timeout=10)
>>> connection.request("HEAD", "/")

>>> response = connection.getresponse()
>>> response.getheaders()
[('Date', 'Tue, 20 Sep 2022 18:10:37 GMT'), ('Content-Type', 'text/html'), ('Content-Length', '178'), ('Connection', 'keep-alive'), ('Cache-Control', 'max-age=600'), ('Location', 'https://www.globo.com/')]
```

Esse código inicia criando uma conexão para uma URL `globo.com` usando a porta padrão HTTP 80. Em seguida, fazemos uma requisição para o caminho padrão "/" usando o método `.request()`. A resposta dessa requisição é obtida pelo método `.getresponse()`. Finalmente, para evitar trazer todo o arquivo do site trazemos somente o HEADER. Se o *request* tiver sucesso, o site está online. Caso contrário, retorná um erro.

Vamos incluir essa lógica em um arquivo `checker.py` que vai lidar com possíveis erros:

```python
# checker.py

from http.client import HTTPConnection
from urllib.parse import urlparse

def site_is_online(url, timeout=10):
    """Return True if the target URL is online.

    Raise an exception otherwise.
    """
    error = Exception("Deu ruim!")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]
    for port in (80, 443):
        connection = HTTPConnection(host=host, port=port, timeout=timeout)
        try:
            connection.request("HEAD", "/")
            return True
        except Exception as e:
            error = e
        finally:
            connection.close()
    raise error
```

Para testar a função recém criada, abra uma sessão interativa no Python e rode o código abaixo:

```python
>>> from sitechecker.checker import site_is_online

>>> site_is_online("indicium.tech")
True

>>> site_is_online("incidium.tech")
```

## 3. Criar o CLI

Para criarmos uma aplicação de linha de comando (*CLI*) vamos usar o `argparse` do python. Para isso, precisamos criar uma classe `ArgumentParser` que recebe argumentos da linha de comando.

```python
# cli.py

import argparse

def read_user_cli_args():

    parser = argparse.ArgumentParser(
        prog="sitechecker", description="Teste a disponibilidade de uma URL"
    )

    parser.add_argument(
        "-u",
        "--urls",
        metavar="URLs",
        nargs="+",
        type=str,
        default=[],
        help="Insira um ou mais URLs"
    )

    parser.add_argument("--file", type=argparse.FileType('r'))

    return parser.parse_args()
```

Já temos uma função que recebe argumentos do CLI, mas ainda precisamos retornar algo para nosso usuário. Para isso vamos clicar uma função que retorna uma mensagem de sucesso se o site estiver online ou de fracasso se o site não está online.

```python
# cli.py
# ...

def display_check_result(result, url, error=""):
    print(f'Os status da "{url}" é:', end =" ")
    if result:
        print('"Online!👍"')
    else:
        print(f'"Offline?" 👎 \n  Erro: "{error}"')

```
## 4. Juntando tudo

Agora chegou a hora de juntar a lógica criada no arquivo `checker.py` com nosso `cli.py`. Para isso vamos criar um arquivo `__main__.py` que permite executar o pacote como um executável usando `python -m <nome_do_pacote>`.

Vamos começar criando uma função `main()` que lê os argumentos do CLI e chamará as demais funções necessárias:

```python
# __main__.py

import sys

from sitechecker.cli import read_user_cli_args

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
```

Logo vemos que esse código não irá rodar porque ainda não definimos a função `_site_check()`. Esta função vai iterar sobre uma lista de URLs obtida dos argumentos do CLI e aplicar a função `site_is_online()` que definimos anteriormente. Em caso de sucesso, ela retornará `True`. E `False` se a consulta retornar um erro. 

```python
# __main__.py

import pathlib
import sys

from sitechecker.cli import read_user_cli_args

def main():
    # ...

def _site_check(urls):
    for url in urls:
        error = ""
        try:
            result = site_is_online(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url.rstrip('\n'), error)
```

Dessa forma, podemos executar a aplicação da seguintes formas: 

1) Para uma ou mais URLs: python __main__.py -u [site1] [site2] ...
2) Para um arquivo CSV: python __main__.py --file [ARQUIVO.csv]
