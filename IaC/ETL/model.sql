CREATE SCHEMA IF NOT EXISTS darwin;

CREATE TABLE IF NOT EXISTS darwin.dim_cliente 
(
    SK_Cliente integer NOT NULL,
    ID_Natural character varying(50) NOT NULL,
    Nome_Cliente character varying(50) NOT NULL,
    Tipo_Cliente character varying(50),
    Situacao character varying(50),
    CONSTRAINT dim_cliente_pkey PRIMARY KEY (SK_Cliente)
);

CREATE TABLE IF NOT EXISTS darwin.dim_localizacao
(
    SK_Localizacao integer NOT NULL,
    ID_Natural character varying(50) NOT NULL,
    Cidade character varying(50) NOT NULL,
    Estado character varying(50) NOT NULL,
    Regiao character varying(50) NOT NULL,
    CONSTRAINT dim_localizacao_pkey PRIMARY KEY (SK_Localizacao)
);

CREATE TABLE IF NOT EXISTS darwin.dim_produto
(
    SK_Produto integer NOT NULL,
    ID_Natural character varying(50) NOT NULL,
    Nome_Produto character varying(255) NOT NULL,
    Categoria_Produto character varying(100) NOT NULL,
    Subcategoria_Produto character varying(100) NOT NULL,
    Marca_Produto character varying(100),
    CONSTRAINT dim_produto_pkey PRIMARY KEY (SK_Produto)
);

CREATE TABLE IF NOT EXISTS darwin.dim_tempo
(
    SK_Tempo integer NOT NULL,
    Data date,
    Ano integer NOT NULL,
    Mes integer NOT NULL,
    Trimestre integer NOT NULL,
    Sazonalidade character varying(50),
    CONSTRAINT dim_tempo_pkey PRIMARY KEY (SK_Tempo)
);

CREATE TABLE IF NOT EXISTS darwin.fato_vendas
(
    ID_Venda integer NOT NULL,
    Quantidade integer NOT NULL,
    Preco_Venda numeric(10,2) NOT NULL,
    Custo_Produto numeric(10,2) NOT NULL,
    SK_Cliente integer NOT NULL,
    SK_Produto integer NOT NULL,
    SK_Localizacao integer NOT NULL,
    SK_Tempo integer NOT NULL,
    Data_Venda date,
    receita_vendas numeric(10,2) NOT NULL,
    CONSTRAINT fato_vendas_pkey PRIMARY KEY (SK_Produto, SK_Cliente, SK_Localizacao, SK_Tempo),
    CONSTRAINT fato_vendas_sk_cliente_fkey FOREIGN KEY (SK_Cliente) REFERENCES darwin.dim_cliente (SK_Cliente),
    CONSTRAINT fato_vendas_sk_localidade_fkey FOREIGN KEY (SK_Localizacao) REFERENCES darwin.dim_localizacao (SK_Localizacao),
    CONSTRAINT fato_vendas_sk_produto_fkey FOREIGN KEY (SK_Produto) REFERENCES darwin.dim_produto (SK_Produto),
    CONSTRAINT fato_vendas_sk_tempo_fkey FOREIGN KEY (SK_Tempo) REFERENCES darwin.dim_tempo (SK_Tempo)
);

COPY darwin.dim_cliente
FROM 's3://darwin-ecommerce-bucket-975050271621/data/Dim_Cliente.csv'
IAM_ROLE 'arn:aws:iam::975050271621:role/RedshiftS3AccessRole'
CSV;

COPY darwin.dim_produto 
FROM 's3://darwin-ecommerce-bucket-975050271621/data/Dim_Produto.csv'
IAM_ROLE 'arn:aws:iam::975050271621:role/RedshiftS3AccessRole'
CSV;

COPY darwin.dim_localizacao
FROM 's3://darwin-ecommerce-bucket-975050271621/data/Dim_Localizacao.csv'
IAM_ROLE 'arn:aws:iam::975050271621:role/RedshiftS3AccessRole'
CSV;

COPY darwin.dim_tempo
FROM 's3://darwin-ecommerce-bucket-975050271621/data/Dim_Tempo.csv'
IAM_ROLE 'arn:aws:iam::975050271621:role/RedshiftS3AccessRole'
CSV;

COPY darwin.fato_vendas
FROM 's3://darwin-ecommerce-bucket-975050271621/data/Fato_Vendas.csv'
IAM_ROLE 'arn:aws:iam::975050271621:role/RedshiftS3AccessRole'
CSV;
