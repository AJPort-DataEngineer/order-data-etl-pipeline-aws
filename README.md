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

<img width="500" height="500" alt="pipeline diagram project1" src="https://github.com/user-attachments/assets/c32d5d21-6af4-415f-a4e6-097b5b19127f" />



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

