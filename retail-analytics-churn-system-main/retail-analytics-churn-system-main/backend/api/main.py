from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("models/churn_model.pkl")

@app.get("/")
def home():
    return {"message": "RIAP Churn Prediction API Running"}

@app.post("/predict")
def predict(recency: float, frequency: float, monetary: float):
    data = np.array([[recency, frequency, monetary]])
    prediction = model.predict(data)[0]
    probability = model.predict_proba(data).max()

    return {
        "prediction": int(prediction),
        "confidence": round(float(probability), 4)
    }