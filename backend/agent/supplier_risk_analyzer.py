from backend.agent.llm_service import LLMService

# Initialize the LLM Service
llm_service = LLMService()
from loguru import logger

def supplier_risk_analyzer_node(state: dict) -> dict:
    prompt_template = """
    system
    You are an AI model for analyzing supplier risk. Given the supplier reliability score, calculate the risk factor. Return only a JSON object with a key 'supplier_risk' containing a float value. Do not include any explanations or additional text.
    user
    Supplier Reliability: {supplier_reliability}
    assistant
    """

    try:
        response = llm_service.generate_response(prompt_template, {
            "supplier_reliability": state['supplier_reliability']
        })
    except ValueError:
        # If the first attempt fails, retry with an explicit JSON instruction
        logger.warning("First attempt failed. Retrying with explicit JSON instruction.")
        response = llm_service.retry_with_json_instruction(prompt_template, {
            "supplier_reliability": state['supplier_reliability']
        })

    supplier_risk = response.get('supplier_risk', 0.0)
    logger.info(f"Supplier risk analyzed: {supplier_risk}")
    state['supplier_risk'] = supplier_risk
    return state