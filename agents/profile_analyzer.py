__module_name__ = "profile_analyzer"

from backend.llm import get_chat_model
from backend.prompts.profile_analysis import get_prompt
from .utils import parse_llm_response, validate_required_params
from typing import Dict

class ProfileAnalyzerAgent:
    def __init__(self):
        self.model = get_chat_model()
        self.prompt_template = get_prompt()

    def analyze(self, linkedin_profile_data: dict) -> Dict[str, any]:
        validate_required_params(linkedin_profile_data=linkedin_profile_data)
        prompt = self.prompt_template.format(linkedin_profile_data=linkedin_profile_data)
        response = self.model.invoke(prompt)
        return parse_llm_response(response)
