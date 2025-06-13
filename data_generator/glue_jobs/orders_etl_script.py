import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load the CSV data from Glue Catalog table
datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database = "my_glue_database",
    table_name = "orders_csv",
    transformation_ctx = "datasource0"
)

# Example transform: Filter only shipped or processing orders
filtered = Filter.apply(frame = datasource0, f = lambda x: x["order_status"] in ["shipped", "processing"])

# Write output as Parquet to S3
glueContext.write_dynamic_frame.from_options(
    frame = filtered,
    connection_type = "s3",
    connection_options = {"path": "s3://my-data-engineering-bucket-aj/orders_parquet/"},
    format = "parquet",
    transformation_ctx = "datasink0"
)

job.commit()
