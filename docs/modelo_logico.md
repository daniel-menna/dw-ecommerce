Aqui está o **Modelo Lógico** atualizado do Data Warehouse (DW) utilizando **Surrogate Keys (chaves substitutas)**. O modelo lógico descreve as tabelas, suas colunas, e os relacionamentos entre elas em um nível intermediário, sem os detalhes físicos, mas considerando as surrogate keys.

### 1. **Tabela de Fato: Fato_Vendas**

A tabela de fato mantém os dados transacionais e utiliza **surrogate keys** (representadas por `SK_`) para fazer referência às tabelas de dimensão. 

| Nome do Campo        | Tipo de Dado | Descrição                                             |
|----------------------|--------------|-------------------------------------------------------|
| **ID_Venda**         | BIGINT       | Identificador único da venda (surrogate key)          |
| **Quantidade_Vendida**| INT          | Quantidade de produtos vendidos                       |
| **Preco_Venda**       | DECIMAL(10,2)| Preço de venda do produto                             |
| **Custo_Produto**     | DECIMAL(10,2)| Custo do produto                                      |
| **Valor_Total_Venda** | DECIMAL(12,2)| Quantidade vendida * Preço de venda                   |
| **SK_Cliente**        | BIGINT       | Surrogate key da dimensão Cliente                     |
| **SK_Produto**        | BIGINT       | Surrogate key da dimensão Produto                     |
| **SK_Localizacao**    | BIGINT       | Surrogate key da dimensão Localização                 |
| **SK_Tempo**          | BIGINT       | Surrogate key da dimensão Tempo                       |
| **Data_Venda**        | DATE         | Data da venda                                         |

#### Relacionamentos:
- **SK_Cliente** -> **Dim_Cliente(SK_Cliente)**
- **SK_Produto** -> **Dim_Produto(SK_Produto)**
- **SK_Localizacao** -> **Dim_Localizacao(SK_Localizacao)**
- **SK_Tempo** -> **Dim_Tempo(SK_Tempo)**

### 2. **Tabela de Dimensão: Dim_Cliente**

A tabela **Dim_Cliente** utiliza uma **surrogate key** (SK_Cliente) como chave primária, e mantém uma coluna de chave natural (ID_Natural) que representa o identificador original do cliente, como CPF ou CNPJ.

| Nome do Campo   | Tipo de Dado | Descrição                              |
|-----------------|--------------|----------------------------------------|
| **SK_Cliente**  | BIGINT       | Surrogate key da dimensão Cliente      |
| **ID_Natural**  | VARCHAR(50)  | Chave natural (ex.: CPF ou CNPJ)       |
| **Nome_Cliente**| VARCHAR(255) | Nome completo do cliente               |
| **Tipo_Cliente**| VARCHAR(50)  | Tipo de cliente (Corporativo ou Consumidor) |
| **Status_Cliente**| VARCHAR(20) | Status do cliente (Ativo, Desativado)  |

#### Chaves e Restrições:
- **SK_Cliente**: Chave primária (surrogate key).
- **ID_Natural**: Deve ser único para garantir que cada cliente tenha uma identificação distinta.

### 3. **Tabela de Dimensão: Dim_Produto**

A tabela **Dim_Produto** também utiliza uma **surrogate key** (SK_Produto), e a chave natural (ID_Natural) representa o código do produto ou SKU.

| Nome do Campo       | Tipo de Dado | Descrição                                  |
|---------------------|--------------|--------------------------------------------|
| **SK_Produto**      | BIGINT       | Surrogate key da dimensão Produto          |
| **ID_Natural**      | VARCHAR(50)  | Chave natural (ex.: Código do Produto, SKU)|
| **Nome_Produto**    | VARCHAR(255) | Nome do produto                            |
| **Categoria_Produto**| VARCHAR(100)| Categoria do produto (ex.: Computadores)   |
| **Subcategoria_Produto**| VARCHAR(100)| Subcategoria do produto (ex.: Notebooks)  |
| **Marca_Produto**   | VARCHAR(100) | Marca do produto                           |

#### Chaves e Restrições:
- **SK_Produto**: Chave primária (surrogate key).
- **ID_Natural**: Deve ser único para garantir que cada produto tenha uma identificação única.

### 4. **Tabela de Dimensão: Dim_Localizacao**

Na tabela **Dim_Localizacao**, a **surrogate key** (SK_Localizacao) é utilizada como chave primária, e a chave natural (ID_Natural) pode ser usada para representar códigos geográficos, se aplicável.

| Nome do Campo    | Tipo de Dado | Descrição                            |
|------------------|--------------|--------------------------------------|
| **SK_Localizacao**| BIGINT       | Surrogate key da dimensão Localização|
| **ID_Natural**   | VARCHAR(50)  | Chave natural (se aplicável)         |
| **Cidade**       | VARCHAR(100) | Cidade onde a venda ocorreu          |
| **Estado**       | VARCHAR(50)  | Estado onde a venda ocorreu          |
| **Regiao**       | VARCHAR(50)  | Região geográfica (ex.: Norte, Sul)  |

#### Chaves e Restrições:
- **SK_Localizacao**: Chave primária (surrogate key).
- **ID_Natural**: Opcional, caso a empresa use códigos de localização únicos.

### 5. **Tabela de Dimensão: Dim_Tempo**

A tabela **Dim_Tempo** utiliza uma **surrogate key** (SK_Tempo) como chave primária. Ela armazena diferentes níveis de granularidade temporal.

| Nome do Campo   | Tipo de Dado | Descrição                                  |
|-----------------|--------------|--------------------------------------------|
| **SK_Tempo**    | BIGINT       | Surrogate key da dimensão Tempo            |
| **Data**        | DATE         | Data exata da venda                        |
| **Mes**         | INT          | Mês da venda                               |
| **Ano**         | INT          | Ano da venda                               |
| **Trimestre**   | INT          | Trimestre da venda (1, 2, 3 ou 4)          |
| **Sazonalidade**| VARCHAR(50)  | Indicação de períodos sazonais (ex.: Natal, Black Friday) |

#### Chaves e Restrições:
- **SK_Tempo**: Chave primária (surrogate key).
- **Data**: Deve ser único para garantir que cada dia esteja representado apenas uma vez.

### 6. **Relacionamentos Entre as Tabelas**

A **tabela de fato** se conecta às **tabelas de dimensão** por meio das surrogate keys. O diagrama do modelo lógico, considerando surrogate keys, pode ser representado assim:

```
                        +-------------------+
                        | Dim_Cliente       |
                        +-------------------+
                        | SK_Cliente        |
                        | ID_Natural        |
                        | Nome_Cliente      |
                        | Tipo_Cliente      |
                        | Status_Cliente    |
                        +-------------------+
                               |
                               |
                               |
     +------------------+      +--------------------+       +-----------------+      +-------------------+
     |  Dim_Tempo        |------|     Fato_Vendas    |-------|  Dim_Produto    |------|  Dim_Localizacao   |
     +------------------+      +--------------------+       +-----------------+      +-------------------+
     |  SK_Tempo         |      |  ID_Venda          |       |  SK_Produto     |      |  SK_Localizacao    |
     |  Data             |      |  Quantidade_Vendida|       |  Nome_Produto   |      |  Cidade            |
     |  Mes              |      |  Preco_Venda       |       |  Categoria_Prod |      |  Estado            |
     |  Ano              |      |  Custo_Produto     |       |  Subcategoria_Prod|    |  Regiao            |
     |  Trimestre        |      |  Valor_Total_Venda |       |  Marca_Produto  |      +-------------------+
     |  Sazonalidade     |      |  SK_Cliente        |       +-----------------+
     +------------------+      |  SK_Produto        |
                                |  SK_Localizacao    |
                                |  SK_Tempo          |
                                +--------------------+
```

### Benefícios do Uso de Surrogate Keys no Modelo Lógico:
1. **Imutabilidade**: Surrogate keys não mudam com o tempo, o que garante a integridade das relações entre tabelas.
2. **Simplicidade**: Surrogate keys são numéricas e sequenciais, o que simplifica as operações de junção e reduz o tamanho dos índices em comparação com chaves naturais que podem ser textos ou compostas.
3. **Flexibilidade**: A inclusão de surrogate keys facilita o tratamento de **dimensões variantes no tempo (SCD - Slowly Changing Dimensions)**, uma vez que é possível associar múltiplas versões de uma dimensão sem afetar o histórico de transações.

Este modelo lógico agora está preparado para ser implementado no nível físico, utilizando surrogate keys, o que garante maior eficiência e escalabilidade ao sistema de Data Warehouse.