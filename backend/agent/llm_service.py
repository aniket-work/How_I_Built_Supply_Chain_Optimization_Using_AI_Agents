import os
import re
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from backend.agent.constant import GROQ_API_KEY, MODEL_NAME

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File: backend/agent/llm_service.py

import os
import re
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from backend.agent.constant import GROQ_API_KEY, MODEL_NAME

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        api_key = os.getenv(GROQ_API_KEY)
        self.llm = ChatGroq(model=MODEL_NAME, groq_api_key=api_key)
        self.json_parser = JsonOutputParser()

    def generate_response(self, prompt_template: str, input_variables: Dict[str, Any]) -> Dict[str, Any]:
        try:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=list(input_variables.keys())
            )
            chain = prompt | self.llm
            response = chain.invoke(input_variables)

            # Log the raw response for debugging
            logger.info(f"Raw response from LLM: {response}")

            # Extract JSON content from the response
            response_text = response.content

            # Try to find JSON in the response
            json_match = re.search(r'^\s*(\{.*\})\s*$', response_text, re.DOTALL)
            if json_match:
                json_content = json_match.group(1)
            else:
                raise ValueError("No valid JSON object found in the response")

            # Attempt to parse JSON content
            try:
                parsed_response = json.loads(json_content)
            except json.JSONDecodeError:
                raise ValueError("Failed to parse JSON from the response")

            return parsed_response

        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            raise

    def retry_with_json_instruction(self, prompt_template: str, input_variables: Dict[str, Any]) -> Dict[str, Any]:
        json_instruction = "\nRemember to respond with a valid JSON object only, without any additional text or explanations."
        new_prompt_template = prompt_template + json_instruction
        return self.generate_response(new_prompt_template, input_variables)