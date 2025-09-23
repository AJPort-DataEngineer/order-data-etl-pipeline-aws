import pandas as pd
from faker import Faker
import uuid
import random
import os

fake = Faker()
statuses = ['shipped', 'processing', 'cancelled', 'returned']

orders = []
for _ in range(100):
    order_id = str(uuid.uuid4())
    customer_id = f"cust_{random.randint(1000, 9999)}"
    order_date = fake.date_between(start_date='-30d', end_date='today')
    order_status = random.choice(statuses)
    total_amount = round(random.uniform(10.0, 500.0), 2)
    shipping_address = fake.address().replace('\n', ', ')
    
    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date,
        "order_status": order_status,
        "total_amount": total_amount,
        "shipping_address": shipping_address
    })

df = pd.DataFrame(orders)

os.makedirs("output", exist_ok=True)
df.to_csv("output/orders.csv", index=False)  # Fixed filename here
print("✅ File generated: output/orders.csv")
