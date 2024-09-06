import random
from faker import Faker
import pandas as pd

# Inicializa o Faker
fake = Faker()

# Lista de nomes reais de produtos
real_product_names = [
    'Produto1',
    'Produto2',
    'Produto3',
    'Produto4',
    'Produto5',
    'Produto6',
    'Produto7',
    'Produto8',
    'Produto9',
    'Produto10',
    'Produto11',
    'Produto12',
    'Produto13'
]

# Funções para gerar as tabelas de dimensão
def generate_dim_cliente(n):
    data = []
    for i in range(1, n + 1):
        cliente = {
            'SK_Cliente': i,
            'ID_Natural': fake.ssn(),  # Usando SSN como equivalente ao CPF/CNPJ
            'Nome_Cliente': fake.name(),
            'Tipo_Cliente': random.choice(['Corporativo', 'Consumidor']),
            'Status_Cliente': random.choice(['Ativo', 'Desativado'])
        }
        data.append(cliente)
    return pd.DataFrame(data)

def generate_dim_produto(n):
    data = []
    for i in range(1, n + 1):
        produto = {
            'SK_Produto': i,
            'ID_Natural': fake.ean(),  # Usando EAN para simular um SKU
            'Nome_Produto': random.choice(real_product_names),  # Nome real de produto
            'Categoria_Produto': random.choice(['Eletrônicos', 'Móveis', 'Roupas', 'Brinquedos']),
            'Subcategoria_Produto': random.choice(['Smartphones', 'Notebooks', 'Mesas', 'Cadeiras', 'Vestidos']),
            'Marca_Produto': fake.company()
        }
        data.append(produto)
    return pd.DataFrame(data)

def generate_dim_localizacao(n):
    data = []
    for i in range(1, n + 1):
        localizacao = {
            'SK_Localizacao': i,
            'ID_Natural': fake.zipcode(),
            'Cidade': fake.city(),
            'Estado': fake.state_abbr(),
            'Regiao': random.choice(['Norte', 'Sul', 'Leste', 'Oeste'])
        }
        data.append(localizacao)
    return pd.DataFrame(data)

def generate_dim_tempo(n):
    data = []
    for i in range(1, n + 1):
        date = fake.date_this_decade()
        tempo = {
            'SK_Tempo': i,
            'Data': date,
            'Mes': date.month,
            'Ano': date.year,
            'Trimestre': (date.month - 1) // 3 + 1,
            'Sazonalidade': random.choice(['Normal', 'Natal', 'Black Friday'])
        }
        data.append(tempo)
    return pd.DataFrame(data)

# Função para gerar a tabela de fato
def generate_fato_vendas(n, clientes, produtos, localizacoes, tempos):
    data = []
    for i in range(1, n + 1):
        venda = {
            'ID_Venda': i,
            'Quantidade_Vendida': random.randint(1, 10),
            'Preco_Venda': round(random.uniform(50.0, 1000.0), 2),
            'Custo_Produto': round(random.uniform(30.0, 700.0), 2),
            'SK_Cliente': random.choice(clientes),
            'SK_Produto': random.choice(produtos),
            'SK_Localizacao': random.choice(localizacoes),
            'SK_Tempo': random.choice(tempos),
            'Data_Venda': fake.date_this_decade()
        }
        venda['Valor_Total_Venda'] = round(venda['Quantidade_Vendida'] * venda['Preco_Venda'], 2)
        data.append(venda)
    return pd.DataFrame(data)

# Gerando as tabelas de dimensão
df_dim_cliente = generate_dim_cliente(100)
df_dim_produto = generate_dim_produto(50)
df_dim_localizacao = generate_dim_localizacao(20)
df_dim_tempo = generate_dim_tempo(365)

# Gerando a tabela de fato
df_fato_vendas = generate_fato_vendas(
    1000,
    df_dim_cliente['SK_Cliente'].tolist(),
    df_dim_produto['SK_Produto'].tolist(),
    df_dim_localizacao['SK_Localizacao'].tolist(),
    df_dim_tempo['SK_Tempo'].tolist()
)

# Salvando os dados em arquivos CSV
df_dim_cliente.to_csv('Dim_Cliente.csv', index=False)
df_dim_produto.to_csv('Dim_Produto.csv', index=False)
df_dim_localizacao.to_csv('Dim_Localizacao.csv', index=False)
df_dim_tempo.to_csv('Dim_Tempo.csv', index=False)
df_fato_vendas.to_csv('Fato_Vendas.csv', index=False)

print("Arquivos CSV salvos com sucesso.")