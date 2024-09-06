Com base no contexto apresentado e no modelo conceitual do Data Warehouse (DW) que detalhamos anteriormente, vamos agora criar o **Modelo Dimensional**. Este modelo, também conhecido como **Modelo Estrela**, é utilizado para permitir a navegação e análise dos dados de maneira eficiente, especialmente para consultas analíticas.

O **Modelo Dimensional** é composto por uma ou mais tabelas de fato, que contêm os dados quantitativos (transações, métricas, etc.), e diversas tabelas de dimensão, que fornecem o contexto para essas medidas.

### 1. **Tabela de Fato (Fato_Vendas)**

A **tabela fato** armazena as transações das vendas realizadas pela empresa, contendo as métricas importantes para análise, como quantidade de produtos vendidos, preço e custos associados. As chaves estrangeiras conectam essa tabela às dimensões associadas.

| Nome do Campo        | Tipo de Dado | Descrição                                             |
|----------------------|--------------|-------------------------------------------------------|
| **ID_Venda**         | Inteiro      | Identificador único da venda                          |
| **Quantidade_Vendida**| Inteiro      | Quantidade de produtos vendidos                       |
| **Preço_Venda**       | Decimal      | Preço pelo qual o produto foi vendido                 |
| **Custo_Produto**     | Decimal      | Custo do produto para a empresa                       |
| **Valor_Total_Venda** | Decimal      | Quantidade vendida * Preço de venda                   |
| **ID_Cliente**        | Inteiro      | Chave estrangeira para a tabela Dimensão Cliente      |
| **ID_Produto**        | Inteiro      | Chave estrangeira para a tabela Dimensão Produto      |
| **ID_Localização**    | Inteiro      | Chave estrangeira para a tabela Dimensão Localização  |
| **ID_Tempo**          | Inteiro      | Chave estrangeira para a tabela Dimensão Tempo        |

### 2. **Tabelas de Dimensão**

As tabelas de dimensão fornecem o contexto para as análises. Cada dimensão armazena informações descritivas que permitem segmentar e detalhar as análises. Abaixo, vamos detalhar cada uma das dimensões do nosso modelo.

#### **Dimensão Cliente**
Esta tabela contém informações sobre os clientes, permitindo que a empresa segmente as vendas por tipo de cliente, status e outras características relevantes.

| Nome do Campo   | Tipo de Dado | Descrição                              |
|-----------------|--------------|----------------------------------------|
| **ID_Cliente**  | Inteiro      | Identificador único do cliente         |
| **Nome_Cliente**| Texto        | Nome do cliente                        |
| **Tipo_Cliente**| Texto        | Tipo do cliente (Corporativo, Consumidor)|
| **Status_Cliente**| Texto      | Status do cliente (Ativo, Desativado)  |

#### **Dimensão Produto**
Essa dimensão contém informações sobre os produtos vendidos, como suas categorias, subcategorias e marcas, permitindo análises detalhadas de performance de produto.

| Nome do Campo       | Tipo de Dado | Descrição                                  |
|---------------------|--------------|--------------------------------------------|
| **ID_Produto**      | Inteiro      | Identificador único do produto             |
| **Nome_Produto**    | Texto        | Nome do produto                            |
| **Categoria_Produto**| Texto       | Categoria do produto (ex.: Notebooks)      |
| **Subcategoria_Produto**| Texto    | Subcategoria do produto (ex.: Ultrabooks)  |
| **Marca_Produto**   | Texto        | Marca do produto (ex.: Apple, Dell)        |

#### **Dimensão Localização**
A dimensão de localização é fundamental para análises geográficas, permitindo à empresa entender melhor a performance das vendas em diferentes regiões do Brasil.

| Nome do Campo    | Tipo de Dado | Descrição                            |
|------------------|--------------|--------------------------------------|
| **ID_Localização**| Inteiro      | Identificador único da localização   |
| **Cidade**       | Texto        | Cidade onde a venda ocorreu          |
| **Estado**       | Texto        | Estado onde a venda ocorreu          |
| **Região**       | Texto        | Região onde a venda ocorreu (ex.: Norte, Sul) |

#### **Dimensão Tempo**
A dimensão de tempo fornece as informações temporais que permitem análises sazonais e por período, como dia, mês, ano, e trimestre.

| Nome do Campo   | Tipo de Dado | Descrição                                  |
|-----------------|--------------|--------------------------------------------|
| **ID_Tempo**    | Inteiro      | Identificador único para a data            |
| **Data**        | Data         | Data exata da venda                        |
| **Mês**         | Inteiro      | Mês da venda                               |
| **Ano**         | Inteiro      | Ano da venda                               |
| **Trimestre**   | Inteiro      | Trimestre da venda (1º, 2º, 3º ou 4º)      |
| **Sazonalidade**| Texto        | Indicação de períodos sazonais (ex.: Natal, Black Friday) |