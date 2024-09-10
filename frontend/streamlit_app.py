import streamlit as st
import requests
import json

# Set the FastAPI backend URL
backend_url = "http://localhost:8000/optimize_supply_chain"

# Streamlit page configuration
st.title("Supply Chain Optimization using AI Agents")
st.write("Enter supply chain details to receive AI-generated recommendations.")

# Inputs for supply chain data
date = st.date_input("Date")
product_id = st.number_input("Product ID", min_value=1, step=1)
historical_demand = st.text_area("Historical Demand (comma-separated)", "100, 120, 140, 160, 180")
current_inventory = st.number_input("Current Inventory", min_value=0.0, value=50.0)
supplier_reliability = st.slider("Supplier Reliability (0 to 1)", min_value=0.0, max_value=1.0, value=0.85)

# Parse the historical demand input into a list of floats
try:
    historical_demand = [float(d.strip()) for d in historical_demand.split(",")]
except ValueError:
    st.error("Please enter valid numbers for historical demand, separated by commas.")
    historical_demand = []

# Button to run optimization
if st.button("Run Optimization"):
    if historical_demand:
        # Prepare the data for the API request
        supply_chain_data = {
            "date": str(date),
            "product_id": int(product_id),
            "historical_demand": historical_demand,
            "current_inventory": current_inventory,
            "supplier_reliability": supplier_reliability
        }

        # Send the data to the FastAPI backend for optimization
        response = requests.post(backend_url, json=supply_chain_data)

        if response.status_code == 200:
            # Display the optimization results
            optimization_result = response.json()
            st.success("Optimization completed successfully!")

            # Display Forecast
            st.subheader("Forecast")
            forecast_data = optimization_result.get('forecast', [])
            if forecast_data:
                st.line_chart(forecast_data)
            else:
                st.write("No forecast data available")

            # Display other results
            st.subheader("Optimization Results")
            st.write(f"Reorder Point: {optimization_result.get('reorder_point', 0.0):.2f}")
            st.write(f"Economic Order Quantity: {optimization_result.get('economic_order_quantity', 0.0):.2f}")
            st.write(f"Supplier Risk: {optimization_result.get('supplier_risk', 0.0):.2f}")

            # Display Recommendations
            st.subheader("Recommendations")
            recommendations = optimization_result.get('recommendations', [])
            if recommendations:
                for rec in recommendations:
                    st.write(f"- {rec}")
            else:
                st.write("No recommendations available")

        else:
            st.error(f"Optimization failed: {response.text}")
    else:
        st.error("Please provide valid historical demand data.")