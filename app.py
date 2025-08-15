# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020
@author: win10
"""

# 1. Library imports
import uvicorn
from fastapi import FastAPI
from customerChurn import CstmrChrn
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import os

# 2. Create the app object
app = FastAPI()

# Load model and scaler
classifier = joblib.load("lrc_bset_model.pkl")
scaler = joblib.load("scaler.pkl")  # StandardScaler for selected columns

# Columns that need scaling
cols_to_scale = ["tenure", "monthlycharges"]

# Log file name
LOG_FILE = "predictions_log.csv"


@app.get("/")
def index():
    return {"This FastAPI created by Md Refat Hosain"}


@app.get("/{name}")
def get_name(name: str):
    return {"Welcome Md Refat's FAST API page. write your name": f"{name}"}


# prediction endpoint
@app.post("/predict")
def predict_churn(data: CstmrChrn):
    # Convert to dict and DataFrame
    data_dict = data.dict()
    df = pd.DataFrame([data_dict])

    # Scale only specific columns
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # Predict
    prediction = classifier.predict(df.values)
    prediction_label = "Churned" if prediction[0] > 0.5 else "Not churned"

    # --- Logging ---
    log_entry = data_dict.copy()
    log_entry["prediction"] = prediction_label
    log_entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists(LOG_FILE):
        # Create CSV with headers if it doesn't exist
        pd.DataFrame([log_entry]).to_csv(LOG_FILE, index=False)
    else:
        # Append without writing headers
        pd.DataFrame([log_entry]).to_csv(LOG_FILE, mode="a", index=False, header=False)

    # Return original input & prediction
    return {"original_input": data_dict, "prediction": prediction_label}


# 6. Run the API
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
