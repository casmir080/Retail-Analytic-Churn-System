from sqlalchemy import text
from backend.db.connection import engine


def trigger_retention_actions():

    query = """
    SELECT customer_id, monetary
    FROM customer_rfm_features
    WHERE churn_risk = 'high'
    """

    with engine.connect() as conn:
        results = conn.execute(text(query)).fetchall()

    print("\n=== RETENTION ACTIONS ===\n")

    for row in results[:10]:
        customer_id, value = row

        action = "Send Discount Offer" if value > 500 else "Send Reminder Email"

        print(f"Customer {customer_id} → {action}")

    print("\nTOTAL HIGH RISK CUSTOMERS:", len(results))


if __name__ == "__main__":
    trigger_retention_actions()