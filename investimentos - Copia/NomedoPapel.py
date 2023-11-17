import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random

import requests
from bs4 import BeautifulSoup

# URL da página com a lista de ações
url = 'https://www.fundamentus.com.br/resultado.php'

# Cabeçalho da requisição para simular um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fazendo a requisição à página com o cabeçalho
response = requests.get(url, headers=headers)

# Verifica se a requisição foi bem-sucedida (código 200)
if response.status_code == 200:
    # Obtendo o conteúdo HTML da página
    html = response.text

    # Analisando o HTML com o BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontrando a tabela que contém as informações das ações
    tabela_acoes = soup.find('table', {'class': 'resultado'})

    # Iterando sobre as linhas da tabela (ignorando o cabeçalho)
    for linha in tabela_acoes.find_all('tr')[1:]:
        # Extraindo as células da linha
        colunas = linha.find_all('td')
        
        # Extraindo as informações desejadas (exemplo: Nome da Empresa e P/L)
        papel = colunas[0].text.strip()
                
        # Imprimindo as informações
        print(f'Papel: {papel}')

        # Aqui você pode continuar extraindo outras informações conforme necessário

else:
    print(f'Erro na requisição. Código de status: {response.status_code}')

