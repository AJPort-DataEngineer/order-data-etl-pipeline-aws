import sys
import json
import logging
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

logger = logging.getLogger("glue")
logger.setLevel(logging.INFO)

def log_event(event_type, message, details=None):
    """Structured JSON logger for CloudWatch"""
    event = {
        "event_type": event_type,
        "message": message,
        "details": details
    }
    print(json.dumps(event))
    logger.info(json.dumps(event))


# Step 1: Load the CSV data from Glue Catalog

log_event("LOAD_START", "Loading data from Glue Catalog")

datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database="my_glue_database",
    table_name="orders_csv",
    transformation_ctx="datasource0"
)

# Convert to Spark DataFrame for data quality checks
df = datasource0.toDF()

row_count = df.count()
log_event("LOAD_SUCCESS", "Loaded data from catalog", {"row_count": row_count})


# Data Quality Checks

log_event("QUALITY_CHECKS_START", "Running data quality validations")

# Row Count Check
if row_count == 0:
    raise ValueError("❌ Data Quality Check Failed: No rows found in dataset")

# Null Value Checks
null_orders = df.filter(col("order_id").isNull()).count()
null_status = df.filter(col("order_status").isNull()).count()
if null_orders > 0 or null_status > 0:
    raise ValueError(
        f"❌ Nulls found in key fields — order_id: {null_orders}, order_status: {null_status}"
    )

# Value Range Check (e.g., ensure price > 0)
if "price" in df.columns:
    invalid_prices = df.filter(col("price") <= 0).count()
    if invalid_prices > 0:
        raise ValueError(f"❌ Found {invalid_prices} rows with invalid price values")

log_event("QUALITY_CHECKS_PASS", "All data quality checks passed successfully")


# Example Transform (Filter only shipped or processing orders)

filtered = Filter.apply(
    frame=datasource0,
    f=lambda x: x["order_status"] in ["shipped", "processing"]
)
log_event("TRANSFORM_SUCCESS", "Filtered shipped and processing orders")


# Write Output as Parquet

output_path = "s3://my-data-engineering-bucket-aj/orders_parquet/"

log_event("WRITE_START", "Writing Parquet data to S3", {"path": output_path})

glueContext.write_dynamic_frame.from_options(
    frame=filtered,
    connection_type="s3",
    connection_options={"path": output_path},
    format="parquet",
    transformation_ctx="datasink0"
)

log_event("WRITE_SUCCESS", "Successfully wrote Parquet data to S3", {"path": output_path})

# Commit Job

job.commit()
log_event("JOB_COMPLETE", "Orders ETL job completed successfully")
