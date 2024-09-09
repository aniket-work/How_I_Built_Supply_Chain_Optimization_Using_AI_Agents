import streamlit as st
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

# AI Agent Imports
from backend.agent.demand_forecaster import DemandForecaster
from backend.agent.inventory_optimizer import InventoryOptimizer
from backend.agent.supplier_risk_analyzer import SupplierRiskAnalyzer
from backend.agent.recommendation_generator import RecommendationGenerator

# FastAPI setup
app = FastAPI()

# Streamlit setup
st.set_page_config(page_title="OptChain Solutions", page_icon="📊", layout="wide")


# Data Models
class SupplyChainData(BaseModel):
    date: str
    product_id: str
    historical_demand: List[float]
    current_inventory: float
    supplier_reliability: float


class OptimizationResult(BaseModel):
    forecast: List[float]
    reorder_point: float
    economic_order_quantity: float
    supplier_risk: float
    recommendations: List[str]


# FastAPI Endpoints
@app.post("/forecast_demand")
async def forecast_demand(data: SupplyChainData):
    agent = DemandForecaster()
    forecast = agent.forecast(data.historical_demand)
    return {"forecast": forecast}


@app.post("/optimize_inventory")
async def optimize_inventory(data: SupplyChainData):
    agent = InventoryOptimizer()
    reorder_point, eoq = agent.optimize(data.historical_demand, data.current_inventory)
    return {"reorder_point": reorder_point, "economic_order_quantity": eoq}


@app.post("/analyze_supplier_risk")
async def analyze_supplier_risk(data: SupplyChainData):
    agent = SupplierRiskAnalyzer()
    risk = agent.analyze(data.supplier_reliability)
    return {"supplier_risk": risk}


@app.post("/generate_recommendations")
async def generate_recommendations(data: OptimizationResult):
    agent = RecommendationGenerator()
    recommendations = agent.generate(data)
    return {"recommendations": recommendations}


# Streamlit UI
def main():
    st.title("OptChain Solutions: Supply Chain Optimization System")

    # Input form
    with st.form("supply_chain_data"):
        date = st.date_input("Date")
        product_id = st.text_input("Product ID")
        historical_demand = st.text_input("Historical Demand (comma-separated values)")
        current_inventory = st.number_input("Current Inventory")
        supplier_reliability = st.slider("Supplier Reliability", 0.0, 1.0, 0.5)

        submitted = st.form_submit_button("Optimize Supply Chain")

    if submitted:
        # Prepare data
        historical_demand = [float(x.strip()) for x in historical_demand.split(",")]
        data = SupplyChainData(
            date=str(date),
            product_id=product_id,
            historical_demand=historical_demand,
            current_inventory=current_inventory,
            supplier_reliability=supplier_reliability
        )

        # Call API endpoints
        forecast_response = requests.post("http://localhost:8000/forecast_demand", json=data.dict())
        inventory_response = requests.post("http://localhost:8000/optimize_inventory", json=data.dict())
        risk_response = requests.post("http://localhost:8000/analyze_supplier_risk", json=data.dict())

        if all(response.status_code == 200 for response in [forecast_response, inventory_response, risk_response]):
            forecast = forecast_response.json()["forecast"]
            reorder_point = inventory_response.json()["reorder_point"]
            eoq = inventory_response.json()["economic_order_quantity"]
            supplier_risk = risk_response.json()["supplier_risk"]

            optimization_result = OptimizationResult(
                forecast=forecast,
                reorder_point=reorder_point,
                economic_order_quantity=eoq,
                supplier_risk=supplier_risk,
                recommendations=[]
            )

            recommendations_response = requests.post("http://localhost:8000/generate_recommendations",
                                                     json=optimization_result.dict())

            if recommendations_response.status_code == 200:
                recommendations = recommendations_response.json()["recommendations"]
                optimization_result.recommendations = recommendations

                # Display results
                st.subheader("Optimization Results")
                st.line_chart(forecast)
                st.metric("Reorder Point", f"{reorder_point:.2f}")
                st.metric("Economic Order Quantity", f"{eoq:.2f}")
                st.metric("Supplier Risk", f"{supplier_risk:.2%}")

                st.subheader("Recommendations")
                for rec in recommendations:
                    st.write(f"• {rec}")
            else:
                st.error("Failed to generate recommendations")
        else:
            st.error("Failed to optimize supply chain")


if __name__ == "__main__":
    import threading


    # Run FastAPI in a separate thread
    def run_fastapi():
        uvicorn.run(app, host="0.0.0.0", port=8000)


    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()

    # Run Streamlit
    main()