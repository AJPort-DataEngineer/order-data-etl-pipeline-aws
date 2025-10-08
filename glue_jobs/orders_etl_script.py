import sys
import json
import logging
import traceback
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col

# -----------------------------------------------------------------------------
# Setup: Contexts and Logging
# -----------------------------------------------------------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

logger = logging.getLogger("glue")
logger.setLevel(logging.INFO)

def log_event(level, message, details=None):
    """Structured JSON log event"""
    event = {
        "level": level,
        "message": message,
        "details": details,
    }
    print(json.dumps(event))  # Glue pushes this to CloudWatch automatically
    logger.info(json.dumps(event))

# -----------------------------------------------------------------------------
# Wrapped ETL Logic with Error Handling
# -----------------------------------------------------------------------------
try:
    log_event("INFO", "Starting Glue ETL job")

    # Step 1: Load data
    datasource0 = glueContext.create_dynamic_frame.from_catalog(
        database="my_glue_database",
        table_name="orders_csv",
        transformation_ctx="datasource0"
    )
    df = datasource0.toDF()
    row_count = df.count()
    log_event("INFO", "Data loaded", {"row_count": row_count})

    # Step 2: Data quality checks
    if row_count == 0:
        raise ValueError("Data Quality Check Failed: Empty dataset")

    null_orders = df.filter(col("order_id").isNull()).count()
    if null_orders > 0:
        raise ValueError(f"Found {null_orders} null order_ids")

    invalid_prices = df.filter(col("price") <= 0).count()
    if invalid_prices > 0:
        raise ValueError(f"Found {invalid_prices} invalid prices")

    log_event("INFO", "Data quality checks passed")

    # Step 3: Transform
    filtered = Filter.apply(
        frame=datasource0,
        f=lambda x: x["order_status"] in ["shipped", "processing"]
    )
    log_event("INFO", "Filtered shipped and processing orders")

    # Step 4: Write
    output_path = "s3://my-data-engineering-bucket-aj/orders_parquet/"
    glueContext.write_dynamic_frame.from_options(
        frame=filtered,
        connection_type="s3",
        connection_options={"path": output_path},
        format="parquet",
        transformation_ctx="datasink0"
    )
    log_event("INFO", "Data written successfully", {"output": output_path})

    job.commit()
    log_event("SUCCESS", "Glue ETL job completed successfully")

except Exception as e:
    error_trace = traceback.format_exc()
    log_event("ERROR", "Glue ETL job failed", {
        "error_message": str(e),
        "stack_trace": error_trace
    })
    job.commit()
    raise
