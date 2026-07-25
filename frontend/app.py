
import streamlit as st
import pandas as pd
import requests

# Replace this with your GitHub Codespaces forwarded URL
BACKEND_URL = "https://YOUR-FORWARDED-URL-7860.app.github.dev"

st.title("SuperKart Sales Forecasting")

st.header("Online Prediction")

product_weight = st.number_input("Product Weight", value=12.0)

product_sugar = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar","Regular","No Sugar"]
)

allocated_area = st.number_input("Allocated Area", value=0.08)

product_type = st.selectbox(
    "Product Type",
    [
        "Dairy",
        "Snack Foods",
        "Frozen Foods",
        "Soft Drinks",
        "Household",
        "Baking Goods",
        "Health and Hygiene",
        "Meat",
        "Canned",
        "Breads",
        "Breakfast",
        "Hard Drinks",
        "Seafood",
        "Fruits and Vegetables",
        "Starchy Foods",
        "Others"
    ]
)

mrp = st.number_input("Product MRP", value=150.0)

store_size = st.selectbox(
    "Store Size",
    ["Small","Medium","High"]
)

city = st.selectbox(
    "Store City Tier",
    ["Tier 1","Tier 2","Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Food Mart",
        "Supermarket Type1",
        "Supermarket Type2"
    ]
)

store_age = st.number_input("Store Age", value=15)

payload = {

    "Product_Weight":product_weight,
    "Product_Sugar_Content":product_sugar,
    "Product_Allocated_Area":allocated_area,
    "Product_Type":product_type,
    "Product_MRP":mrp,
    "Store_Size":store_size,
    "Store_Location_City_Type":city,
    "Store_Type":store_type,
    "Store_Age":store_age

}

if st.button("Predict Sales"):

    response = requests.post(

        f"{BACKEND_URL}/v1/sales",

        json=payload

    )

    if response.status_code==200:

        st.success(response.json()["Predicted Sales"])

    else:

        st.error("Backend API not reachable")



st.header("Batch Prediction")

uploaded_file = st.file_uploader("Upload CSV",type=["csv"])

if uploaded_file:

    if st.button("Predict Batch"):

        response=requests.post(

            f"{BACKEND_URL}/v1/salesbatch",

            files={"file":uploaded_file}

        )

        if response.status_code==200:

            st.write(response.json())

        else:

            st.error("Prediction Failed")
