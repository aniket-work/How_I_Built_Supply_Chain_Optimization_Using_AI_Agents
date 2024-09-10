import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, TypedDict
import uvicorn
from loguru import logger

# Importing nodes (AI agent nodes as separate files)
from .agent.demand_forecaster import demand_forecaster_node
from .agent.inventory_optimizer import inventory_optimizer_node
from .agent.supplier_risk_analyzer import supplier_risk_analyzer_node
from .agent.recommendation_generator import recommendation_generator_node

load_dotenv()

# Define the FastAPI app
app = FastAPI()


from pydantic import BaseModel
from typing import List

class ForecastItem(BaseModel):
    date: int
    demand: float

class OptimizationResult(BaseModel):
    forecast: List[ForecastItem]
    reorder_point: float
    economic_order_quantity: float
    supplier_risk: float
    recommendations: List[str]
    current_inventory: float

class SupplyChainData(BaseModel):
    date: str
    product_id: int
    historical_demand: list[float]
    current_inventory: float
    supplier_reliability: float


class SupplyChainResponse(BaseModel):
    forecast: List[ForecastItem]
    reorder_point: float
    economic_order_quantity: float
    supplier_risk: float
    recommendations: List[str]
    current_inventory: float

# Workflow State Definition
class SupplyChainState(TypedDict):
    date: str
    product_id: str
    historical_demand: List[float]
    current_inventory: float
    supplier_reliability: float
    forecast: List[float]
    reorder_point: float
    economic_order_quantity: float
    supplier_risk: float
    recommendations: List[str]

# Setup LangGraph Workflow with the AI agent nodes
workflow = StateGraph(SupplyChainState)

# Add each node to the workflow
workflow.add_node("demand_forecaster", demand_forecaster_node)
workflow.add_node("inventory_optimizer", inventory_optimizer_node)
workflow.add_node("supplier_risk_analyzer", supplier_risk_analyzer_node)
workflow.add_node("recommendation_generator", recommendation_generator_node)

# Define the entry point of the workflow
workflow.set_entry_point("demand_forecaster")

# Define the flow between nodes
workflow.add_edge("demand_forecaster", "inventory_optimizer")
workflow.add_edge("inventory_optimizer", "supplier_risk_analyzer")
workflow.add_edge("supplier_risk_analyzer", "recommendation_generator")
workflow.add_edge("recommendation_generator", END)

# Compile the workflow
compiled_app = workflow.compile()

# API Endpoint to optimize the supply chain using FastAPI


@app.post("/optimize_supply_chain", response_model=OptimizationResult)
async def optimize_supply_chain(data: SupplyChainData):
    try:
        # Initialize the state with the provided data
        state = {
            "date": data.date,
            "product_id": data.product_id,
            "historical_demand": data.historical_demand,
            "current_inventory": data.current_inventory,
            "supplier_reliability": data.supplier_reliability,
            "forecast": [],
            "reorder_point": 0.0,
            "economic_order_quantity": 0.0,
            "supplier_risk": 0.0,
            "recommendations": []
        }

        # Run the workflow
        for s in compiled_app.stream(state):
            logger.info(f"Step completed: {list(s.keys())[0]}")
            logger.info(f"Current state: {s}")

            # Extract the final state after the workflow finishes
            final_state = s[list(s.keys())[0]]
            logger.info(f"Final state after workflow: {final_state}")

            # Convert forecast to list of ForecastItem
            forecast_items = [
                ForecastItem(date=i, demand=d)
                for i, d in enumerate(final_state.get('forecast', []))
            ]

        result = OptimizationResult(
            forecast=forecast_items,
            reorder_point=final_state.get('reorder_point', 0.0),
            economic_order_quantity=final_state.get('economic_order_quantity', 0.0),
            supplier_risk=final_state.get('supplier_risk', 0.0),
            recommendations=final_state.get('recommendations', []),
            current_inventory=final_state.get('current_inventory', 0.0)
        )

        return result
    except Exception as e:
        logger.error(f"Error in optimization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
