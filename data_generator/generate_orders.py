import pandas as pd
import uuid
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_orders(num_orders=100):
    orders = []
    for _ in range(num_orders):
        order_id = str(uuid.uuid4())
        customer_id = str(uuid.uuid4())
        order_date = fake.date_time_between(start_date='-30d', end_date='now')
        order_status = fake.random_element(elements=('shipped', 'processing', 'cancelled', 'returned'))
        total_amount = round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)
        shipping_address = fake.address().replace('\n', ', ')
        
        orders.append({
            'order_id': order_id,
            'customer_id': customer_id,
            'order_date': order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'order_status': order_status,
            'total_amount': total_amount,
            'shipping_address': shipping_address
        })
    
    df = pd.DataFrame(orders)
    df.to_csv('output/orders.csv', index=False)
    print(f"Generated {num_orders} orders and saved to output/orders.csv")

if __name__ == "__main__":
    generate_orders()
