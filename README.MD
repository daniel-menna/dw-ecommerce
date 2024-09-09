# Modeling a Data Warehouse for an Ecommerce Company using AWS, Metabase and Terraform

In this prooject I defined the following architecture to execute it.
![Architecture Defined](./pics/architecture.png)

## Context
A company in the e-commerce sector operates across various regions in Brazil, selling a variety of technology products, such as computers, smartphones, and peripherals. The company serves both corporate clients and individual consumers. The company is interested in monitoring and analyzing its sales to understand customer behavior, product performance, and regional trends over time.

### Objective:
The company aims to build a data analytics system that allows detailed collection and analysis of sales. This includes the ability to segment data by customer, location, product, and time period. The system should assist in strategic decision-making, such as launching new promotions, adjusting inventory, and expanding into new regions.

### Details of the Company’s Operations:
The company sells technology products to its customers, who may be either individual consumers or businesses. Each sale is associated with a specific customer and takes place in a specific geographic location. The system needs to record the product sold, the quantity, the sale price, and the cost of the product.

Further details about how this project was designed are availables in my [Article at Medium](https://www.medium.com/@data-menna)

## Tech Stack Used
- Python
- Docker and Docker-Compose
- Terraform
- Metabase
- Amazon S3
- Amazon Redshift
- Github

## Before Executing the Project
To execute this project, it is necessary to follow the following steps:

### Install Docker
[Install Docker for your OS](https://docs.docker.com/desktop/)

### Install Docker-Compose
[Install Docker-Compose for your OS](https://docs.docker.com/compose/install/)

### Clone this Github repository
In your terminal:

Clone the repo using Github CLI or Git CLI
```
gh repo clone daniel-menna/dw-ecommerce
```
or

```
git clone https://www.github.com/daniel-menna/dw-ecommerce.git
```
Open the folder with your code editor.

## Preparing Everithing
To run this project without any headake, it is necessary to follow few steps:

### Create a S3 Bucket
In your browser go to [https://aws.amazon.com//s3/](https://aws.amazon.com//s3/) and create a bucket, recomended something like: `ecommerce-dw-bucket-<YOUR-ID-AWS>`.

Copy your bucket name and save it for later.

### Generate your Data Source
In the project folder, you can generate your data source following these steps:
- Access the `src` folder;
- Run the Python script called `faker_datas.py`.
    ```
    python run faker_datas.py
    ```
    Note: It is necessary to have Python installed in your environment. If you don't want to run this script, you can find sample file in the `data` folder, in this repository.
- Create a folder `data` in you S3 Bucket and upload these files there.

### Build the project
Execute the following command in the terminal:
```
docker-compose up
```

## Executing the project
With your container successfully implemented, access it and open the container terminal.

### Configure your AWS CLI
In the terminal run `aws configure` and set your pair of keys, it will ensure that your keys are not avbailable in any place of the codebase.

### Access the project folder
Execute the following comand to access the `Infra` folder:
```
cd IaC/Infra
```

### Creating the Infrastructure
To create the infra using Terraform, execute the following comands:

```
terraform init
terraform validate #Check if the syntax is correct to execute Terraform
terraform plan #Check all the infrastructure to be created
terraform apply
```

### Checking the Deploy
Access the [Redshift Console](https://console.aws.amazon.com/redshiftv2/home) and confirm if the Cluster `darwindb`is created.

Copy the endpoint for the redshift instance, you will use it soon.

After that access the [IAM Console](https://console.aws.amazon.com/iam/home#/home) and check the IAM ID created.

Copy this ID and save it, we will use it later.

### Database schema creation
Into the folder `ETL`, in the project folder (local machine), edit the file called `model.sql` and make the following changes:
- Update the ACCOUNT ID to your own ID at AWS;
- Update the bucket name accordingly.

To execute the schema creation, update the redshift endpoind in the comand below to your own:

```
psql -h redshift-cluster.cjsicv1vrjsq.us-east-2.redshift.amazonaws.com -U adminuser -d dsadb -p 5439 -f model.sql
```

Now, exceute this comand into your container, in the folder `ETL`.

## Outputs
Now, it is possible to check the tables created in Redshift using the web console.

### Metabase
Go to the [http://localhost:3000/](http://localhost:3000/) and create your local account. When the `Add your data` option shows up, choose `Redshift`, and enter your details. It will ask for a `Display name`, I recomend `Ecommerce-DW` or something like that. 

Include the database credentials and your are ready to analyze the data!

## Contact
- [Linkedin](https://www.linkedin.com/in/daniel-menna)
- [Github](https://www.github.com/daniel-menna)
- [danielmenna@gmail.com](mailto:danielmenna@gmail.com)

Please, feel free to reach out to me for any suggestion, issue or bug fix needed. All contributions are welcome!
