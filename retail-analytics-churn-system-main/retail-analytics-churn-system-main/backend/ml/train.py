import pandas as pd
from sqlalchemy import text
from backend.db.connection import engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
import joblib


def load_data():
    return pd.read_sql("SELECT * FROM customer_rfm_features", engine)


def prepare_data(df):
    mapping = {"low": 0, "medium": 1, "high": 2}
    df["churn_label"] = df["churn_risk"].map(mapping)

    features = [
        "recency",
        "frequency",
        "monetary",
        "avg_order_value",
        "order_span",
        "purchase_rate"
    ]

    df = df.fillna(0)

    X = df[features]
    y = df["churn_label"]

    return X, y


def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("\n--- Logistic Regression ---\n")
    lr = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=2000))
    ])
    lr.fit(X_train, y_train)
    preds_lr = lr.predict(X_test)
    print(classification_report(y_test, preds_lr))

    print("\n--- XGBoost ---\n")
    xgb = XGBClassifier(eval_metric="mlogloss")
    xgb.fit(X_train, y_train)
    preds_xgb = xgb.predict(X_test)
    print(classification_report(y_test, preds_xgb))

    return xgb


def save_model(model):
    joblib.dump(model, "models/churn_model.pkl")
    print("BEST MODEL SAVED")


if __name__ == "__main__":
    df = load_data()
    X, y = prepare_data(df)
    model = train_models(X, y)
    save_model(model)