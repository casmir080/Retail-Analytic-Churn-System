import pandas as pd
import os

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)


def validate_customers():
    df = pd.read_csv(f"{RAW_PATH}/customers.csv")

    required_cols = ["customer_id", "customer_name", "email", "signup_date", "country"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df["email"] = df["email"].fillna("unknown@email.com")

    df["country"] = df["country"].str.lower()

    country_map = {
        "us": "usa",
        "united states": "usa",
        "uk": "uk"
    }

    df["country"] = df["country"].replace(country_map)

    df = df.drop_duplicates(subset=["customer_id"])


    df.to_csv(f"{PROCESSED_PATH}/customers_clean.csv", index=False)

    print("CUSTOMERS VALIDATED")


def run_validation():
    validate_customers()


if __name__ == "__main__":
    run_validation()
if __name__ == "__main__":
    print("RUNNING VALIDATION...")
    run_validation()