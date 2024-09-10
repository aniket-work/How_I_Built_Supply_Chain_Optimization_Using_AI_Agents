import numpy as np
from sklearn.ensemble import RandomForestRegressor

from backend.agent.llm_service import LLMService
from loguru import logger
# Initialize the LLM Service
llm_service = LLMService()

# Define the agents as nodes that interact with the LLM

def demand_forecaster_node(state: dict) -> dict:
    prompt_template = """
    system
    You are an AI model for forecasting demand based on historical data. Given historical demand data, generate forecasts for the next 30 days. Return the forecasts as a JSON object with a key 'forecast' containing a list of floats. Do not include any explanation or code, just the JSON object.
    user
    Historical Demand: {historical_demand}
    assistant
    """

    response = llm_service.generate_response(prompt_template, {
        "historical_demand": state['historical_demand']
    })

    forecast = response.get('forecast', [])
    logger.info(f"Forecast generated: {forecast}")
    state['forecast'] = forecast
    return state


