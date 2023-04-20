# Web Connectivity Test 💻

Aplicação Python para validar se um URL está online ou offline e retornar uma mensagem para o usuário.

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

## 2. Verificador de sites

O arquivo `checker.py` é a responsável para a verificação e está demonstrada abaixo:

```python
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
```
Nela, utilizamos a biblioteca requests para fazer a checagem e a biblioteca colocama para mudarmos a cor dos textos de resposta. 

A função site_is_online irá verificar se o argumento digitado pelo usuário está iniciado com o `http` ou não. Caso não, ele irá adicionar o `https://` para que o resquests.get não retorne erro.

Enfim, caso o `status_code` do site for 200, então ele está online. Caso contrário, estará offline.

## 3. CLI

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
Nesse caso, o usuário poderá iniciar a aplicação com argumentos de URLs (-u) ou com argumento de arquivo (--file).

## 4. Construindo a aplicação principal

Nesse momento, fazemos a execução da lógica criada no arquivo `checker.py` com nosso `cli.py`. Para isso vamos criar um arquivo `__main__.py` que permite executar o pacote como um executável usando `python <nome_do_pacote>`.

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

Logo vemos que esse código não irá rodar porque ainda não definimos a função `_site_check()`. Esta função vai iterar sobre uma lista de URLs obtida dos argumentos do CLI e aplicar a função `site_is_online()` que definimos anteriormente.

```python
# __main__.py

import pathlib
import sys

from sitechecker.cli import read_user_cli_args

def main():
    # ...
 
def _site_check(urls):
    for url in urls:
        result = site_is_online(url.rstrip('\n'))
        
if __name__ == "__main__":
    main()
```

## 5. Execução da aplicação em duas formas distintas:

1) Para uma ou mais URLs: ```python __main__.py -u [site1] [site2] ...```

Exemplo de resposta: 

```python
python .\sitechecker\ -u https://googlezdxsdasdasd.com google.com indicium.tech siasdiasd.br google.com
```

![image](https://user-images.githubusercontent.com/13797593/233221961-7d95fd0a-e783-4783-a5d7-b36968e55c04.png)

2) Para um arquivo CSV: ```python __main__.py --file [ARQUIVO.csv]```

Exemplo de resposta: 

```python
python .\sitechecker\ --file .\sitechecker\list.csv
```

![image](https://user-images.githubusercontent.com/13797593/233221673-e8d4a72f-9673-4d6f-b882-0fe4b40d0fc7.png)

## 6. Agendamento da cron job para o Windows:

➡️ Abra o Painel de Controle do Windows e depois clique nas **Administrative Tools**.

➡️ Clique duas vezes no **Task Scheduler** e depois escolha a opção 'Create Basic Task…'.

➡️ Digite um nome para sua tarefa (você também pode digitar uma descrição, se necessário), e então pressione **Next**.

➡️ Escolha iniciar a tarefa '**Daily**' e especifique o horário de execução desejado.

➡️ Selecione, **Start a program** e pressione **Next**.

➡️ Use o botão **Browse** para encontrar o arquivo de lote (cronjob_windows.bat) que executa o script Python.

➡️ Finalmente, clique em **Finish**. A partir deste ponto, o programa será executado no horário informado.
