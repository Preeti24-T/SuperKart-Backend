
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask application
app = Flask(__name__)

# Load trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "SuperKart_Sales_Forecasting_Model.pkl")

model = joblib.load(MODEL_PATH)


# Home Page
@app.route("/", methods=["GET"])
def home():
    return "Welcome to SuperKart Sales Forecasting API"


# -----------------------------
# Online Prediction
# -----------------------------
@app.route("/v1/sales", methods=["POST"])
def predict_sales():

    data = request.get_json()

    input_df = pd.DataFrame([data])

    prediction = model.predict(input_df)[0]

    return jsonify(
        {
            "Predicted Sales": round(float(prediction),2)
        }
    )


# -----------------------------
# Batch Prediction
# -----------------------------
@app.route("/v1/salesbatch", methods=["POST"])
def predict_sales_batch():

    file = request.files["file"]

    batch_data = pd.read_csv(file)

    predictions = model.predict(batch_data)

    output = {}

    for i, pred in enumerate(predictions):

        output[str(i)] = round(float(pred),2)

    return jsonify(output)


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=7860)
