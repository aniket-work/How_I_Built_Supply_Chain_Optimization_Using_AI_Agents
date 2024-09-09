import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="OptChain Solutions", page_icon="📊", layout="wide")

st.title("OptChain Solutions: Supply Chain Optimization System")

with st.form("supply_chain_data"):
    date = st.date_input("Date")
    product_id = st.text_input("Product ID")
    historical_demand = st.text_input("Historical Demand (comma-separated values)")
    current_inventory = st.number_input("Current Inventory")
    supplier_reliability = st.slider("Supplier Reliability", 0.0, 1.0, 0.5)

    submitted = st.form_submit_button("Optimize Supply Chain")

if submitted:
    historical_demand = [float(x.strip()) for x in historical_demand.split(",")]
    data = {
        "date": str(date),
        "product_id": product_id,
        "historical_demand": historical_demand,
        "current_inventory": current_inventory,
        "supplier_reliability": supplier_reliability
    }

    response = requests.post(f"{BACKEND_URL}/optimize_supply_chain", json=data)

    if response.status_code == 200:
        result = response.json()

        st.subheader("Optimization Results")

        # Demand Forecast
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=historical_demand, mode='lines', name='Historical Demand'))
        fig.add_trace(go.Scatter(y=result['forecast'], mode='lines', name='Forecasted Demand'))
        fig.update_layout(title='Demand Forecast', xaxis_title='Time', yaxis_title='Demand')
        st.plotly_chart(fig)

        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Reorder Point", f"{result['reorder_point']:.2f}")
        col2.metric("Economic Order Quantity", f"{result['economic_order_quantity']:.2f}")
        col3.metric("Supplier Risk", f"{result['supplier_risk']:.2%}")

        # Recommendations
        st.subheader("Recommendations")
        for rec in result['recommendations']:
            st.write(f"• {rec}")
    else:
        st.error("Failed to optimize supply chain. Please try again.")