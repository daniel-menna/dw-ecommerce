O **modelo físico** para a implementação do Data Warehouse (DW) no **Amazon Redshift** precisa ser otimizado para o ambiente distribuído e em coluna desse banco de dados. Redshift é altamente otimizado para consultas analíticas e grandes volumes de dados, utilizando técnicas como compressão de colunas, sort keys (chaves de ordenação) e distribuição dos dados entre nós de cluster.

### Considerações Gerais para Amazon Redshift:
- **Surrogate Keys**: São recomendadas para chaves primárias e estrangeiras, como no caso de dimensões e fatos.
- **Distribuição de Dados**: Redshift oferece opções para a distribuição dos dados entre os nós de processamento (por chave, chave composta ou todos os nós).
- **Sort Keys**: Utilizadas para otimizar consultas e a ordenação de dados nas colunas.
- **Compressão**: Redshift permite compressão automática para otimizar o armazenamento e melhorar o desempenho.
- **Primary/Foreign Keys**: São mantidas para documentação e boas práticas, mas não são rigorosamente aplicadas em termos de consistência referencial.

### Modelo Físico no Amazon Redshift

#### 1. **Tabela de Fato: Fato_Vendas**

A tabela de fato no Redshift utilizará **surrogate keys** para referenciar as dimensões. A estratégia de **distribuição** será feita por uma chave que equilibre as consultas (como `SK_Produto` ou `SK_Cliente`), e a **sort key** será definida em colunas frequentemente usadas para filtros e agregações, como `Data_Venda` ou `SK_Tempo`.

```sql
CREATE TABLE Fato_Vendas (
    ID_Venda            BIGINT          IDENTITY(1,1), -- Surrogate key (auto increment)
    Quantidade_Vendida  INT             NOT NULL,      -- Quantidade de produtos vendidos
    Preco_Venda         DECIMAL(12, 2)  NOT NULL,      -- Preço de venda do produto
    Custo_Produto       DECIMAL(12, 2)  NOT NULL,      -- Custo do produto
    Valor_Total_Venda   DECIMAL(14, 2)  DEFAULT NULL,  -- Valor total da venda (calculado externamente ou via ETL)
    SK_Cliente          BIGINT          NOT NULL,      -- Surrogate key para a dimensão Cliente
    SK_Produto          BIGINT          NOT NULL,      -- Surrogate key para a dimensão Produto
    SK_Localizacao      BIGINT          NOT NULL,      -- Surrogate key para a dimensão Localização
    SK_Tempo            BIGINT          NOT NULL,      -- Surrogate key para a dimensão Tempo
    Data_Venda          DATE            NOT NULL,      -- Data da venda
    PRIMARY KEY (ID_Venda)
)
DISTSTYLE KEY                    -- Distribuição dos dados por chave
DISTKEY (SK_Produto)             -- Distribui por SK_Produto para balancear consultas que envolvem produtos
SORTKEY (Data_Venda);            -- Ordena pela Data_Venda para otimizar consultas temporais
```

#### 2. **Tabela de Dimensão: Dim_Cliente**

Na dimensão **Dim_Cliente**, a **distribuição** será definida como `ALL`, já que esta dimensão será relativamente pequena e pode ser replicada em todos os nós do cluster para otimizar as consultas. Usaremos `SK_Cliente` como chave primária.

```sql
CREATE TABLE Dim_Cliente (
    SK_Cliente      BIGINT          IDENTITY(1,1) PRIMARY KEY,  -- Surrogate key da dimensão Cliente
    ID_Natural      VARCHAR(50)     NOT NULL,                   -- Chave natural (ex.: CPF ou CNPJ)
    Nome_Cliente    VARCHAR(255)    NOT NULL,                   -- Nome completo do cliente
    Tipo_Cliente    VARCHAR(50)     NOT NULL,                   -- Tipo de cliente (Corporativo ou Consumidor)
    Status_Cliente  VARCHAR(20)     NOT NULL                    -- Status do cliente (Ativo ou Desativado)
)
DISTSTYLE ALL;  -- Distribui a tabela para todos os nós, otimizando joins com a tabela de fato
```

#### 3. **Tabela de Dimensão: Dim_Produto**

A dimensão **Dim_Produto** terá uma **sort key** na coluna `ID_Natural` para otimizar consultas por SKU ou código de produto, e será distribuída por **`SK_Produto`**.

```sql
CREATE TABLE Dim_Produto (
    SK_Produto          BIGINT          IDENTITY(1,1) PRIMARY KEY, -- Surrogate key da dimensão Produto
    ID_Natural          VARCHAR(50)     NOT NULL,                  -- Chave natural (ex.: Código do Produto, SKU)
    Nome_Produto        VARCHAR(255)    NOT NULL,                  -- Nome do produto
    Categoria_Produto   VARCHAR(100)    NOT NULL,                  -- Categoria do produto (ex.: Computadores)
    Subcategoria_Produto VARCHAR(100)   NOT NULL,                  -- Subcategoria do produto (ex.: Notebooks)
    Marca_Produto       VARCHAR(100)    NOT NULL                   -- Marca do produto
)
DISTSTYLE KEY                    -- Distribui a tabela por chave
DISTKEY (SK_Produto)             -- Distribui por SK_Produto para balancear as consultas de produtos
SORTKEY (ID_Natural);            -- Ordena pela chave natural (ex.: SKU) para otimizar as buscas
```

#### 4. **Tabela de Dimensão: Dim_Localizacao**

A dimensão **Dim_Localizacao** será replicada em todos os nós (`DISTSTYLE ALL`) devido ao seu tamanho potencialmente pequeno e para otimizar as junções com a tabela de fato.

```sql
CREATE TABLE Dim_Localizacao (
    SK_Localizacao   BIGINT          IDENTITY(1,1) PRIMARY KEY, -- Surrogate key da dimensão Localização
    ID_Natural       VARCHAR(50),                              -- Chave natural (se aplicável)
    Cidade           VARCHAR(100)    NOT NULL,                 -- Cidade onde a venda ocorreu
    Estado           VARCHAR(50)     NOT NULL,                 -- Estado onde a venda ocorreu
    Regiao           VARCHAR(50)     NOT NULL                  -- Região geográfica (ex.: Norte, Sul, Sudeste)
)
DISTSTYLE ALL;  -- Distribui a tabela para todos os nós, otimizando joins
```

#### 5. **Tabela de Dimensão: Dim_Tempo**

A dimensão **Dim_Tempo** será usada em quase todas as consultas analíticas, então deve ser replicada em todos os nós para otimizar o desempenho.

```sql
CREATE TABLE Dim_Tempo (
    SK_Tempo        BIGINT          IDENTITY(1,1) PRIMARY KEY, -- Surrogate key da dimensão Tempo
    Data            DATE            NOT NULL,                 -- Data exata da venda
    Mes             INT             NOT NULL,                 -- Mês da venda
    Ano             INT             NOT NULL,                 -- Ano da venda
    Trimestre       INT             NOT NULL,                 -- Trimestre (1, 2, 3 ou 4)
    Sazonalidade    VARCHAR(50)                                -- Indicação de períodos sazonais (ex.: Natal, Black Friday)
)
DISTSTYLE ALL;  -- Distribui a tabela para todos os nós
```

### 6. **Outras Considerações Técnicas para Redshift**

#### **Chaves Primárias e Estrangeiras**
Redshift não aplica chaves primárias e estrangeiras para manter a consistência referencial automaticamente, mas elas podem ser incluídas no modelo para documentação e referência, ajudando nas otimizações do planner de consultas.

#### **Distribuição de Dados**
- **DISTSTYLE KEY**: Usado em tabelas de fato e dimensões maiores (como `Fato_Vendas` e `Dim_Produto`), permitindo que as linhas sejam distribuídas de forma eficiente entre os nós, com base na chave especificada.
- **DISTSTYLE ALL**: Usado para dimensões pequenas (como `Dim_Cliente`, `Dim_Tempo`, `Dim_Localizacao`), onde a replicação em todos os nós melhora o desempenho de consultas que envolvem essas tabelas.

#### **Sort Keys**
- **Sort Key** nas colunas mais utilizadas para filtros e joins, como `Data_Venda` e `SK_Produto`, ajuda a melhorar a eficiência nas buscas e agregações.
- **Sort Keys Compostas** podem ser usadas quando há múltiplas colunas envolvidas em filtros, por exemplo, `(Data_Venda, SK_Produto)`.

#### **Compressão**
- Redshift utiliza automaticamente compressão de colunas para economizar espaço e melhorar o desempenho de leitura. Podemos permitir que o Redshift determine a melhor compressão usando o comando `ANALYZE COMPRESSION`.

```sql
ANALYZE COMPRESSION Fato_Vendas;
ANALYZE COMPRESSION Dim_Produto;
```

### Resumo do Modelo Físico no Redshift:
1. **Fato_Vendas**: Distribuído por **SK_Produto**, sort key por **Data_Venda**.
2. **Dim_Cliente**, **Dim_Localizacao**, e **Dim_Tempo**: Replicadas em todos os nós com **DISTSTYLE ALL**.
3. **Dim_Produto**: Distribuído por **SK_Produto**, sort key por **ID_Natural** (SKU).

Esse modelo físico é otimizado para **Amazon Redshift**, utilizando a distribuição e compressão nativas para maximizar o desempenho em consultas analíticas, mantendo flexibilidade e escalabilidade conforme o volume de dados cresce.