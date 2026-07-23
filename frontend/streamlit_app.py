import streamlit as st
import pandas as pd
import requests
import json

# --- Configuration ---
# Replace with your actual deployed model URL
MODEL_API_URL = "https://probable-parakeet-6vvjpx56q7v5fj9v-7860.app.github.dev/v1/customer"

st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- Sidebar for Navigation/Info ---
st.sidebar.title("About")
st.sidebar.info(
    "This application predicts SuperKart sales based on product and store characteristics. "
    "It uses a machine learning model deployed as a Flask API." 
    "You can adjust the input features on the left to get a sales prediction."
)

st.sidebar.subheader("API Endpoint")
st.sidebar.markdown(f"`{MODEL_API_URL}`")

# --- Main Application ---
st.title("🛒 SuperKart Sales Prediction")
st.write("Enter the details below to get a sales forecast for your product in a store.")

# --- Input Features ---
st.header("Product Details")
product_weight = st.number_input("Product Weight", min_value=4.0, max_value=22.0, value=12.5, step=0.1)

product_sugar_content = st.selectbox(
    "Product Sugar Content", 
    ['Low Sugar', 'Regular', 'No Sugar', 'reg'] # 'reg' included as per EDA
)

product_allocated_area = st.number_input("Product Allocated Area", min_value=0.004, max_value=0.298, value=0.08, step=0.001)

product_type = st.selectbox(
    "Product Type", 
    [
        'Frozen Foods', 'Dairy', 'Canned', 'Baking Goods', 'Health and Hygiene', 
        'Snack Foods', 'Meat', 'Household', 'Hard Drinks', 'Fruits and Vegetables',
        'Breads', 'Soft Drinks', 'Breakfast', 'Others', 'Starchy Foods', 'Seafood'
    ]
)

product_mrp = st.number_input("Product MRP (Max Retail Price)", min_value=31.0, max_value=266.0, value=180.0, step=0.1)

st.header("Store Details")
store_age = st.slider("Store Age (Years)", min_value=15, max_value=38, value=15)

store_size = st.selectbox(
    "Store Size", 
    ['Medium', 'High', 'Small']
)

store_location_city_type = st.selectbox(
    "Store Location City Type", 
    ['Tier 1', 'Tier 2', 'Tier 3']
)

store_type = st.selectbox(
    "Store Type", 
    ['Supermarket Type1', 'Supermarket Type2', 'Departmental Store', 'Food Mart']
)

# --- Prediction Button ---
if st.button("Predict Sales"):    
    # Prepare payload
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_Type": product_type,
        "Product_MRP": product_mrp,
        "Store_Age": store_age,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type,
    }

    # Display payload for debugging
    st.subheader("Sending Request Payload:")
    st.json(payload)

    try:
        # Make POST request to the API
        response = requests.post(MODEL_API_URL, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors

        prediction_result = response.json()
        
        st.success(f"Predicted Product Store Sales: {prediction_result['Predicted Product Store Sales']:.2f}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the API: {e}")
        if response is not None:
            st.text(f"API Response Status: {response.status_code}")
            st.text(f"API Response Body: {response.text}")
    except json.JSONDecodeError:
        st.error(f"Failed to decode JSON from API response. Response was: {response.text}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Optional: Display current feature values
# st.subheader("Current Input Values:")
# st.write(f"Product Weight: {product_weight}")
# st.write(f"Product Sugar Content: {product_sugar_content}")
# st.write(f"Product Allocated Area: {product_allocated_area}")
# st.write(f"Product Type: {product_type}")
# st.write(f"Product MRP: {product_mrp}")
# st.write(f"Store Age: {store_age}")
# st.write(f"Store Size: {store_size}")
# st.write(f"Store Location City Type: {store_location_city_type}")
# st.write(f"Store Type: {store_type}")
