from sqlalchemy import text
from backend.db.connection import engine


def create_feature_table():

    query = """
    CREATE TABLE IF NOT EXISTS customer_order_features AS
    SELECT
        c.customer_id,
        c.customer_name,
        c.country,

        o.order_id,
        o.order_date,
        o.status,

        p.product_id,
        p.product_name,
        p.category,
        p.price,

        oi.quantity,
        oi.total_price,

        (oi.quantity * p.price) AS computed_revenue

    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON oi.product_id = p.product_id
    """

    with engine.begin() as conn:   
        conn.execute(text("DROP TABLE IF EXISTS customer_order_features"))
        conn.execute(text(query))

    print("FEATURE TABLE CREATED")


if __name__ == "__main__":
    create_feature_table()