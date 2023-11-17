import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# URL da página com a lista de ações
url_lista_acoes = 'https://www.fundamentus.com.br/resultado.php'

# Cabeçalho da requisição para simular um navegador
headers_lista_acoes = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fazendo a requisição à página com o cabeçalho
response_lista_acoes = requests.get(url_lista_acoes, headers=headers_lista_acoes)

# Verifica se a requisição foi bem-sucedida (código 200)
if response_lista_acoes.status_code == 200:
    # Obtendo o conteúdo HTML da página
    html_lista_acoes = response_lista_acoes.text

    # Analisando o HTML com o BeautifulSoup
    soup_lista_acoes = BeautifulSoup(html_lista_acoes, 'html.parser')

    # Encontrando a tabela que contém as informações das ações
    tabela_acoes = soup_lista_acoes.find('table', {'class': 'resultado'})

    # Lista para armazenar os códigos das ações
    codigos_acoes = []

    # Dicionário para armazenar informações das ações
    acoes_info = {}

    # Iterando sobre as linhas da tabela (ignorando o cabeçalho)
    for linha in tabela_acoes.find_all('tr')[1:]:
        # Extraindo as células da linha
        colunas = linha.find_all('td')

        # Extraindo as informações desejadas (exemplo: Nome da Empresa e P/L)
        papel = colunas[0].text.strip()

        # Adicionando o código da ação à lista
        codigos_acoes.append(papel)

        # Aqui você pode continuar extraindo outras informações conforme necessário
        # (por exemplo, P/L, Dividend Yield, ROE)

        # Exemplo: Armazenando algumas informações em um dicionário
        try:
            pl_str = colunas[2].text.replace('.', '').replace(',', '.')
            pl = float(pl_str)
        except ValueError:
            pl = 0.0  # Tratando o caso em que o valor não é numérico

        try:
            roe_str = colunas[16].text.replace('.', '').replace(',', '.').replace('%', '')
            roe = float(roe_str)
        except ValueError:
            roe = 0.0  # Tratando o caso em que o valor não é numérico

        info = {
            'PL': pl,
            'DividendYield': float(colunas[5].text.replace(',', '').replace('%', '')) / 100,  # Converte para decimal
            'ROE': roe,
            # Adicione mais informações conforme necessário
        }
        acoes_info[papel] = info

else:
    print(f'Erro na requisição. Código de status: {response_lista_acoes.status_code}')

# Lógica para calcular o rank com base nos critérios
rank_acoes = []

for codigo_acao in codigos_acoes:
    # Aqui você deve adicionar a lógica para calcular o rank conforme os critérios
    # Exemplo: (PL > 0), (Dividend Yield > 5% e < 20%), (ROE > algum_valor)

    # Substitua os valores abaixo pelos critérios específicos que você deseja
    criterio_pl = acoes_info[codigo_acao]['PL'] > 0
    criterio_dividend_yield = 5 < acoes_info[codigo_acao]['DividendYield'] < 20
    criterio_roe = acoes_info[codigo_acao]['ROE'] > 0  # Substitua por algum valor específico

    # Lógica de priorização
    prioridade = criterio_pl + criterio_dividend_yield + criterio_roe

    # Adiciona ao rank
    rank_acoes.append((codigo_acao, prioridade))

# Ordena o rank com base na prioridade
rank_acoes = sorted(rank_acoes, key=lambda x: x[1], reverse=True)

# Imprime o rank
print("Rank de Ações:")
for i, (codigo_acao, prioridade) in enumerate(rank_acoes, start=1):
    print(f"{i}. {codigo_acao} - Prioridade: {prioridade}")
