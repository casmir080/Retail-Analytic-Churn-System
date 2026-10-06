import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("postgresql://riap_user:riap_pass@localhost:5433/riap_db")


def calculate_psi(expected, actual, bins=10):
    expected_percents, _ = np.histogram(expected, bins=bins)
    actual_percents, _ = np.histogram(actual, bins=bins)

    expected_percents = expected_percents / len(expected)
    actual_percents = actual_percents / len(actual)

    psi = np.sum((actual_percents - expected_percents) *
                 np.log((actual_percents + 1e-6) / (expected_percents + 1e-6)))

    return psi


def run_drift_check():
    df = pd.read_sql("SELECT * FROM customer_rfm_features", engine)

    baseline = df.sample(frac=0.5, random_state=42)
    current = df.sample(frac=0.5, random_state=7)

    psi_score = calculate_psi(baseline["monetary"], current["monetary"])

    print("\nPSI SCORE:", psi_score)

    if psi_score > 0.25:
        print("⚠️ Significant drift detected")
    else:
        print("✅ No major drift")


if __name__ == "__main__":
    run_drift_check()