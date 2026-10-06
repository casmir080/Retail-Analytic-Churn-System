from sqlalchemy import text
from backend.db.connection import engine


def build_rfm_features():

    drop_query = "DROP TABLE IF EXISTS customer_rfm_features;"

    create_query = """
    CREATE TABLE customer_rfm_features AS
    SELECT
        customer_id,
        (CURRENT_DATE - MAX(order_date)) AS recency,
        COUNT(DISTINCT order_id) AS frequency,
        SUM(total_price) AS monetary,
        AVG(total_price) AS avg_order_value,
        (MAX(order_date) - MIN(order_date)) AS order_span,
        COUNT(DISTINCT order_id) / NULLIF((MAX(order_date) - MIN(order_date)), 0) AS purchase_rate
    FROM customer_order_features
    WHERE order_date IS NOT NULL
    GROUP BY customer_id;
    """

    with engine.begin() as conn:  
        conn.execute(text(drop_query))
        conn.execute(text(create_query))

    print("RFM FEATURES CREATED")


def add_churn_labels():

    alter_query = """
    ALTER TABLE customer_rfm_features
    ADD COLUMN IF NOT EXISTS churn_risk TEXT;
    """

    update_query = """
    UPDATE customer_rfm_features
    SET churn_risk =
        CASE
            WHEN recency > 90 THEN 'high'
            WHEN recency BETWEEN 30 AND 90 THEN 'medium'
            ELSE 'low'
        END;
    """

    with engine.begin() as conn: 
        conn.execute(text(alter_query))
        conn.execute(text(update_query))

    print("CHURN LABELS ADDED")


if __name__ == "__main__":
    build_rfm_features()
    add_churn_labels()