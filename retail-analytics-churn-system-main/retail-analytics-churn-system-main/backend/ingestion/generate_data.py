import pandas as pd
import random
from datetime import datetime, timedelta
import os

os.makedirs("data/raw", exist_ok=True)

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 50
NUM_ORDERS = 2000

# ------------------------
# CUSTOMERS
# ------------------------
customers = []
countries = ["USA", "us", "United States", "UK", "uk", "Nigeria"]

for i in range(NUM_CUSTOMERS):
    customers.append({
        "customer_id": i + 1,
        "customer_name": f"Customer_{i+1}",
        "email": None if random.random() < 0.1 else f"user{i}@email.com",
        "signup_date": datetime.now() - timedelta(days=random.randint(0, 1000)),
        "country": random.choice(countries)
    })

df_customers = pd.DataFrame(customers)

# introduce duplicates
df_customers = pd.concat([df_customers, df_customers.sample(20)])

# ------------------------
# PRODUCTS
# ------------------------
categories = ["Electronics", "electronics", "Clothing", "clothes"]

products = []
for i in range(NUM_PRODUCTS):
    products.append({
        "product_id": i + 1,
        "product_name": f"Product_{random.randint(1,40)}",  # duplicates
        "category": random.choice(categories),
        "price": round(random.uniform(10, 500), 2)
    })

df_products = pd.DataFrame(products)

statuses = ["Completed", "completed", "DONE", "pending"]

orders = []
for i in range(NUM_ORDERS):
    orders.append({
        "order_id": i + 1,
        "customer_id": random.randint(1, NUM_CUSTOMERS),
        "order_date": None if random.random() < 0.05 else datetime.now() - timedelta(days=random.randint(0, 365)),
        "status": random.choice(statuses)
    })

df_orders = pd.DataFrame(orders)


order_items = []
for i in range(NUM_ORDERS):
    quantity = random.randint(1, 5)

    order_items.append({
        "order_item_id": i + 1,
        "order_id": i + 1,
        "product_id": random.randint(1, NUM_PRODUCTS),
        "quantity": quantity,
        "total_price": quantity * random.uniform(10, 500)
    })

df_order_items = pd.DataFrame(order_items)


df_customers.to_csv("data/raw/customers.csv", index=False)
df_products.to_csv("data/raw/products.csv", index=False)
df_orders.to_csv("data/raw/orders.csv", index=False)
df_order_items.to_csv("data/raw/order_items.csv", index=False)

print("DATA GENERATED SUCCESSFULLY")