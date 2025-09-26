# Variables
PYTHON=python3
BUCKET?=my-batchstream-orders
REGION?=us-east-1

# Default target
all: upload

# Create virtual environment and install dependencies
setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

# Generate synthetic order data
generate:
	$(PYTHON) scripts/generate_orders.py

# Upload generated data to S3
upload: generate
	$(PYTHON) scripts/upload_to_s3.py --bucket $(BUCKET) --region $(REGION)

# Clean generated data
clean:
	rm -f data/*.csv
