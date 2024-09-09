```sql
CREATE SCHEMA IF NOT EXISTS darwin;

CREATE TABLE IF NOT EXISTS darwin.dim_customer 
(
    SK_Customer integer NOT NULL,
    Natural_ID character varying(50) NOT NULL,
    Customer_Name character varying(50) NOT NULL,
    Customer_Type character varying(50),
    Status character varying(50),
    CONSTRAINT dim_customer_pkey PRIMARY KEY (SK_Customer)
);

CREATE TABLE IF NOT EXISTS darwin.dim_location
(
    SK_Location integer NOT NULL,
    Natural_ID character varying(50) NOT NULL,
    City character varying(50) NOT NULL,
    State character varying(50) NOT NULL,
    Region character varying(50) NOT NULL,
    CONSTRAINT dim_location_pkey PRIMARY KEY (SK_Location)
);

CREATE TABLE IF NOT EXISTS darwin.dim_product
(
    SK_Product integer NOT NULL,
    Natural_ID character varying(50) NOT NULL,
    Product_Name character varying(255) NOT NULL,
    Product_Category character varying(100) NOT NULL,
    Product_Subcategory character varying(100) NOT NULL,
    Product_Brand character varying(100),
    CONSTRAINT dim_product_pkey PRIMARY KEY (SK_Product)
);

CREATE TABLE IF NOT EXISTS darwin.dim_time
(
    SK_Time integer NOT NULL,
    Date date,
    Year integer NOT NULL,
    Month integer NOT NULL,
    Quarter integer NOT NULL,
    Seasonality character varying(50),
    CONSTRAINT dim_time_pkey PRIMARY KEY (SK_Time)
);

CREATE TABLE IF NOT EXISTS darwin.fact_sales
(
    Sale_ID integer NOT NULL,
    Quantity integer NOT NULL,
    Sale_Price numeric(10,2) NOT NULL,
    Product_Cost numeric(10,2) NOT NULL,
    SK_Customer integer NOT NULL,
    SK_Product integer NOT NULL,
    SK_Location integer NOT NULL,
    SK_Time integer NOT NULL,
    Sale_Date date,
    sales_revenue numeric(10,2) NOT NULL,
    CONSTRAINT fact_sales_pkey PRIMARY KEY (SK_Product, SK_Customer, SK_Location, SK_Time),
    CONSTRAINT fact_sales_sk_customer_fkey FOREIGN KEY (SK_Customer) REFERENCES darwin.dim_customer (SK_Customer),
    CONSTRAINT fact_sales_sk_location_fkey FOREIGN KEY (SK_Location) REFERENCES darwin.dim_location (SK_Location),
    CONSTRAINT fact_sales_sk_product_fkey FOREIGN KEY (SK_Product) REFERENCES darwin.dim_product (SK_Product),
    CONSTRAINT fact_sales_sk_time_fkey FOREIGN KEY (SK_Time) REFERENCES darwin.dim_time (SK_Time)
);
```