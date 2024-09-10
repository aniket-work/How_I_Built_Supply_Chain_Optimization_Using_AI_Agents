
from backend.agent.llm_service import LLMService

# Initialize the LLM Service
llm_service = LLMService()
from loguru import logger

def recommendation_generator_node(state: dict) -> dict:
    prompt_template = """
    system
    You are an AI model for generating recommendations based on supply chain optimization results. Given forecast, reorder point, EOQ, supplier risk, and current inventory, provide actionable recommendations. Return only a JSON object with a key 'recommendations' containing a list of strings. Do not include any explanations or additional text.
    user
    Forecast: {forecast}
    Reorder Point: {reorder_point}
    Economic Order Quantity: {economic_order_quantity}
    Supplier Risk: {supplier_risk}
    Current Inventory: {current_inventory}
    assistant
    """

    try:
        response = llm_service.generate_response(prompt_template, {
            "forecast": state['forecast'],
            "reorder_point": state['reorder_point'],
            "economic_order_quantity": state['economic_order_quantity'],
            "supplier_risk": state['supplier_risk'],
            "current_inventory": state['current_inventory']
        })
    except ValueError:
        # If the first attempt fails, retry with an explicit JSON instruction
        logger.warning("First attempt failed. Retrying with explicit JSON instruction.")
        response = llm_service.retry_with_json_instruction(prompt_template, {
            "forecast": state['forecast'],
            "reorder_point": state['reorder_point'],
            "economic_order_quantity": state['economic_order_quantity'],
            "supplier_risk": state['supplier_risk'],
            "current_inventory": state['current_inventory']
        })

    recommendations = response.get('recommendations', [])
    logger.info(f"Recommendations generated: {recommendations}")
    state['recommendations'] = recommendations
    return state
