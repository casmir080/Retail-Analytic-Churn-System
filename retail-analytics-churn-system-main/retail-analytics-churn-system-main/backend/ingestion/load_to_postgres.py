import pandas as pd
from sqlalchemy import text
from backend.db.connection import engine

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"


def load_customers():
    df = pd.read_csv(f"{PROCESSED_PATH}/customers_clean.csv")

    data = df.to_dict(orient="records")

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO customers (customer_id, customer_name, email, signup_date, country)
            VALUES (:customer_id, :customer_name, :email, :signup_date, :country)
            ON CONFLICT (customer_id) DO NOTHING
        """), data)

    print("CUSTOMERS LOADED")


def load_products():
    df = pd.read_csv(f"{RAW_PATH}/products.csv")

    data = df.to_dict(orient="records")

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO products (product_id, product_name, category, price)
            VALUES (:product_id, :product_name, :category, :price)
            ON CONFLICT (product_id) DO NOTHING
        """), data)

    print("PRODUCTS LOADED")


def load_orders():
    df = pd.read_csv(f"{RAW_PATH}/orders.csv")

    df["order_date"] = df["order_date"].where(pd.notnull(df["order_date"]), None)

    data = df.to_dict(orient="records")

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO orders (order_id, customer_id, order_date, status)
            VALUES (:order_id, :customer_id, :order_date, :status)
            ON CONFLICT (order_id) DO NOTHING
        """), data)

    print("ORDERS LOADED")


def load_order_items():
    df = pd.read_csv(f"{RAW_PATH}/order_items.csv")

    data = df.to_dict(orient="records")

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO order_items (order_item_id, order_id, product_id, quantity, total_price)
            VALUES (:order_item_id, :order_id, :product_id, :quantity, :total_price)
            ON CONFLICT (order_item_id) DO NOTHING
        """), data)

    print("ORDER ITEMS LOADED")


def run_load():
    load_products()
    load_customers()
    load_orders()
    load_order_items()


if __name__ == "__main__":
    run_load()