from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("SuperKart_Sales_Forecasting_Model.pkl")

@app.route("/")
def home():
    return "Welcome to SuperKart Sales Prediction API"

@app.route("/v1/customer", methods=["POST"])
def predict():

    data = request.get_json()

    input_df = pd.DataFrame([data])

    prediction = model.predict(input_df)[0]

    return jsonify({
        "Predicted Product Store Sales": round(float(prediction),2)
    })


@app.route("/v1/customerbatch", methods=["POST"])
def batch_predict():

    file = request.files["file"]

    df = pd.read_csv(file)

    predictions = model.predict(df)

    df["Predicted Sales"] = predictions

    return df["Predicted Sales"].to_json()


if __name__=="__main__":
    app.run(host="0.0.0.0",port=7860)
