Here is the translation of the provided dimensional model markdown content:

---

Based on the presented context and the conceptual model of the Data Warehouse (DW) we detailed earlier, let's now create the **Dimensional Model**. This model, also known as the **Star Schema**, is used to efficiently navigate and analyze data, especially for analytical queries.

The **Dimensional Model** consists of one or more fact tables, which contain quantitative data (transactions, metrics, etc.), and several dimension tables, which provide context for these measures.

### 1. **Fact Table (Sales_Fact)**

The **fact table** stores the sales transactions conducted by the company, containing important metrics for analysis, such as the number of products sold, prices, and associated costs. Foreign keys link this table to the associated dimensions.

| Field Name            | Data Type  | Description                                          |
|-----------------------|------------|------------------------------------------------------|
| **Sale_ID**           | Integer    | Unique identifier for the sale                       |
| **Quantity_Sold**     | Integer    | Quantity of products sold                            |
| **Sale_Price**        | Decimal    | Price at which the product was sold                  |
| **Product_Cost**      | Decimal    | Cost of the product to the company                   |
| **Total_Sale_Value**  | Decimal    | Quantity sold * Sale price                           |
| **Customer_ID**       | Integer    | Foreign key to the Customer Dimension table          |
| **Product_ID**        | Integer    | Foreign key to the Product Dimension table           |
| **Location_ID**       | Integer    | Foreign key to the Location Dimension table          |
| **Time_ID**           | Integer    | Foreign key to the Time Dimension table              |

### 2. **Dimension Tables**

Dimension tables provide context for the analysis. Each dimension stores descriptive information that allows for segmentation and detailed analysis. Below, we detail each of the dimensions in our model.

#### **Customer Dimension**
This table contains information about customers, enabling the company to segment sales by customer type, status, and other relevant characteristics.

| Field Name        | Data Type  | Description                                 |
|-------------------|------------|---------------------------------------------|
| **Customer_ID**   | Integer    | Unique identifier for the customer          |
| **Customer_Name** | Text       | Customer's name                             |
| **Customer_Type** | Text       | Customer type (Corporate, Consumer)         |
| **Customer_Status**| Text      | Customer status (Active, Inactive)          |

#### **Product Dimension**
This dimension contains information about the products sold, such as their categories, subcategories, and brands, allowing detailed performance analysis of products.

| Field Name           | Data Type  | Description                                   |
|----------------------|------------|-----------------------------------------------|
| **Product_ID**       | Integer    | Unique identifier for the product             |
| **Product_Name**     | Text       | Product name                                  |
| **Product_Category** | Text       | Product category (e.g., Laptops)              |
| **Product_Subcategory**| Text     | Product subcategory (e.g., Ultrabooks)        |
| **Product_Brand**    | Text       | Product brand (e.g., Apple, Dell)             |

#### **Location Dimension**
The location dimension is crucial for geographic analysis, enabling the company to better understand sales performance in different regions of the country.

| Field Name           | Data Type  | Description                                   |
|----------------------|------------|-----------------------------------------------|
| **Location_ID**      | Integer    | Unique identifier for the location            |
| **City**             | Text       | City where the sale occurred                  |
| **State**            | Text       | State where the sale occurred                 |
| **Region**           | Text       | Region where the sale occurred (e.g., North, South) |

#### **Time Dimension**
The time dimension provides the temporal information needed for seasonal and period analysis, such as day, month, year, and quarter.

| Field Name           | Data Type  | Description                                   |
|----------------------|------------|-----------------------------------------------|
| **Time_ID**          | Integer    | Unique identifier for the date                |
| **Date**             | Date       | Exact date of the sale                        |
| **Month**            | Integer    | Month of the sale                             |
| **Year**             | Integer    | Year of the sale                              |
| **Quarter**          | Integer    | Quarter of the sale (1st, 2nd, 3rd, or 4th)   |
| **Seasonality**      | Text       | Indication of seasonal periods (e.g., Christmas, Black Friday) |