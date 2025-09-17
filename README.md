## 👤 About Me

Data Engineer with hands-on experience building cloud-native data pipelines using AWS services. Passionate about transforming raw data into insights.

📍 Based in Dallas, TX  
🎓 B.S. in Cybersecurity / Information Assurance  
💼 Open to data engineering, cloud, or analytics roles   
🔗 LinkedIn: www.linkedin.com/in/ajahne-austin-90576715a 
📧 Contact: austinaj9@gmail.com

End-to-end serverless data pipeline on AWS using Python, S3, Glue, Athena, Lambda, and QuickSight
# AWS Data Engineering Portfolio Project

Overview
This project demonstrates an end-to-end data engineering pipeline using Python and AWS services including S3, Glue, Athena, Lambda, EventBridge, and QuickSight.

<img width="400" height="400" alt="pipeline diagram project1" src="https://github.com/user-attachments/assets/c32d5d21-6af4-415f-a4e6-097b5b19127f" />

⚡ Setup

1. Prerequisites

-AWS Account with permissions for S3, Glue, Athena, IAM, and EventBridge

-IAM User/Role with these policies:

   AmazonS3FullAccess

   AWSGlueServiceRole

   AmazonAthenaFullAccess

   CloudWatchLogsFullAccess

-Local Environment

   Python 3.9+

   Install dependencies: pip install -r requirements.txt

2. Configuration
   Copy to json file: 
    {
     "aws_region": "us-east-1",
     "s3_bucket": "my-batchstream-orders",
     "database_name": "orders_db",
     "table_name": "orders_table"
   }

📊 Schema and Sample data

Schema:
| Column           | Type      | Example                   |
| -----------------| --------- | ------------------------- |
| order_id         | STRING    | `72b25b4d-348b-4fc0-8deb` |
| customer_name    | STRING    | `Ryan Yang`               |
| product_category | STRING    | `Gaming Laptop`           |
| quantity         | INT       | `4`                       |
| price            | DOUBLE    | `424.59`                  |
| order_date       | TIMESTAMP | `2023-09-01 12:34:56`     |

Sample Rows:
| order_id  | customer_name  | product_category  | quantity | price  | order_date  |
| --------- | -------------- | ----------------- | -------- | ------ | ----------- |
| 1a2b...   | Ryan Yang      | Gaming Laptop     | 4        | 424.59 | 2023-09-01  |
| 2b3c...   | Sarah Lee      | Smartphone        | 1        | 799.99 | 2023-09-02  |

🧑‍💻 Example Athena Queries

1. Top 5 Product Categories by Revenue
   SELECT product_category, SUM(quantity * price) AS revenue
   FROM orders_table
   GROUP BY product_category
   ORDER BY revenue DESC
   LIMIT 5;

2. Monthly order volume trend
   SELECT DATE_TRUNC('month', order_date) AS month, COUNT(*) AS total_orders
   FROM orders_table
   GROUP BY month
   ORDER BY month;
 
3. Average order value by customer
   SELECT customer_name, AVG(quantity * price) AS avg_order_value
   FROM orders_table
   GROUP BY customer_name
   ORDER BY avg_order_value DESC
   LIMIT 10;

💾 Partitioning & File Format

-Converted CSV to Parquet for compression + query efficiency.

-Partitioned by order_date (year/month) for time-based filtering.

-Result: Queries run 3–5x faster, with lower Athena costs.

💰 Cost & Limits

-Estimated Monthly Cost (small scale):

   S3: <$1 for GBs of data

   Glue Crawler + ETL: $2–5

   Athena: ~$1 per 1TB scanned (Parquet minimizes this)

   QuickSight: $9/user/month

-Service Limits:

   Athena query timeout = 30 minutes

   Glue job max DPU = 100 (default 10)

   S3 request limits = practically unlimited for this scale

📈 Dashboards



Project Steps
1. Data Generation  
   Synthetic order data generated with Python using Faker and saved as CSV.

2. Data Upload 
   Uploaded CSV files to AWS S3 bucket using Python boto3 library.

3. Data Cataloging  
   Used AWS Glue Crawler to automatically catalog the CSV files in S3.

4. Data Transformation  
   AWS Glue ETL job (PySpark) transformed the data to Parquet format for efficient querying.

5. Data Querying  
   Queried transformed data using AWS Athena.

6. Data Visualization  
   Created interactive dashboards in AWS QuickSight to analyze orders and customers.

7. Automation  
   Automated the workflow using AWS Lambda and EventBridge to trigger crawlers and ETL jobs on new file uploads.

## How to Run
- Clone this repo
- Run `generate_orders.py` to create synthetic CSV data
- Run `upload_to_s3.py` to upload data to your S3 bucket

## Tools & Technologies
- Python (pandas, faker, boto3)
- AWS S3, Glue, Athena, Lambda, EventBridge, QuickSight
- PySpark for Glue ETL jobs

## Contact
For questions or collaboration, reach out via austinaj9@gmail.com.

