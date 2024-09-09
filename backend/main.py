from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

from .agent.demand_forecaster import DemandForecaster
from .agent.inventory_optimizer import InventoryOptimizer
from .agent.supplier_risk_analyzer import SupplierRiskAnalyzer
from .agent.recommendation_generator import RecommendationGenerator

app = FastAPI()

class SupplyChainData(BaseModel):
    date: str
    product_id: str
    historical_demand: List[float]
    current_inventory: float
    supplier_reliability: float

from pydantic import BaseModel, Field

class OptimizationResult(BaseModel):
    forecast: List[float] = Field(...)
    reorder_point: float = Field(...)
    economic_order_quantity: float = Field(...)
    supplier_risk: float = Field(...)
    recommendations: List[str] = Field(default_factory=list)
    current_inventory: float = Field(...)

@app.post("/optimize_supply_chain", response_model=OptimizationResult)
async def optimize_supply_chain(data: SupplyChainData):
    demand_forecaster = DemandForecaster()
    inventory_optimizer = InventoryOptimizer()
    risk_analyzer = SupplierRiskAnalyzer()
    recommendation_generator = RecommendationGenerator()

    forecast = demand_forecaster.forecast(data.historical_demand)
    reorder_point, eoq = inventory_optimizer.optimize(data.historical_demand, data.current_inventory)
    supplier_risk = risk_analyzer.analyze(data.supplier_reliability)

    optimization_result = OptimizationResult(
        forecast=forecast,
        reorder_point=reorder_point,
        economic_order_quantity=eoq,
        supplier_risk=supplier_risk,
        recommendations=[],
        current_inventory=data.current_inventory
    )

    recommendations = recommendation_generator.generate(optimization_result)
    optimization_result.recommendations = recommendations

    return optimization_result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)