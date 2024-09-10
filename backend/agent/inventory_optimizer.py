import numpy as np

from backend.agent.llm_service import LLMService

# Initialize the LLM Service
llm_service = LLMService()
from loguru import logger

# File: backend/agent/inventory_optimizer.py

from backend.agent.llm_service import LLMService
from loguru import logger

# Initialize the LLM Service
llm_service = LLMService()

def inventory_optimizer_node(state: dict) -> dict:
    prompt_template = """
    system
    You are an AI model for optimizing inventory levels. Given historical demand and current inventory, calculate the reorder point and economic order quantity (EOQ). Return only a JSON object with keys 'reorder_point' and 'economic_order_quantity', both containing float values. Do not include any explanations or additional text.
    user
    Historical Demand: {historical_demand}
    Current Inventory: {current_inventory}
    assistant
    """

    try:
        response = llm_service.generate_response(prompt_template, {
            "historical_demand": state['historical_demand'],
            "current_inventory": state['current_inventory']
        })
    except ValueError:
        # If the first attempt fails, retry with an explicit JSON instruction
        logger.warning("First attempt failed. Retrying with explicit JSON instruction.")
        response = llm_service.retry_with_json_instruction(prompt_template, {
            "historical_demand": state['historical_demand'],
            "current_inventory": state['current_inventory']
        })

    state['reorder_point'] = response.get('reorder_point', 0.0)
    state['economic_order_quantity'] = response.get('economic_order_quantity', 0.0)
    logger.info(f"Inventory optimization results: Reorder Point = {state['reorder_point']}, EOQ = {state['economic_order_quantity']}")
    return state