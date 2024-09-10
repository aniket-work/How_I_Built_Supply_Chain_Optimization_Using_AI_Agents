import streamlit as st
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

# FastAPI setup
from fastapi import FastAPI

app = FastAPI()

class SupplyChainData(BaseModel):
    historical_demand: List[float]
    current_inventory: float
    supplier_reliability: float

@app.post("/optimize_supply_chain", response_model=OptimizationResult)
async def optimize_supply_chain(data: SupplyChainData):
    # Initialize workflow state with input data
    initial_state = {
        "historical_demand": data.historical_demand,
        "current_inventory": data.current_inventory,
        "supplier_reliability": data.supplier_reliability
    }

    # Run the LangGraph workflow
    final_state = workflow.run(initial_state)

    # Build the optimization result from the final state
    optimization_result = OptimizationResult(
        forecast=final_state['forecast'],
        reorder_point=final_state['reorder_point'],
        economic_order_quantity=final_state['economic_order_quantity'],
        supplier_risk=final_state['supplier_risk'],
        recommendations=final_state['recommendations'],
        current_inventory=data.current_inventory
    )

    return optimization_result

# Main entry point for running FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)