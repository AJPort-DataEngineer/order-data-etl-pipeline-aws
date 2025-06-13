import boto3
import os

glue = boto3.client('glue')

def lambda_handler(event, context):
    crawler_name = os.environ.get('CRAWLER_NAME', 'orders-csv-crawler')
    job_name = os.environ.get('GLUE_JOB_NAME', 'orders-etl-job')
    
    # Start Glue crawler
    try:
        glue.start_crawler(Name=crawler_name)
        print(f"Started crawler: {crawler_name}")
    except glue.exceptions.CrawlerRunningException:
        print(f"Crawler {crawler_name} is already running")
    except Exception as e:
        print(f"Error starting crawler: {e}")
    
    # Start Glue ETL job
    try:
        glue.start_job_run(JobName=job_name)
        print(f"Started Glue job: {job_name}")
    except Exception as e:
        print(f"Error starting Glue job: {e}")
    
    return {
        'statusCode': 200,
        'body': 'Glue crawler and job triggered successfully'
    }
