__module_name__ = "career_guide"

from backend.llm import get_chat_model
from backend.prompts.career_guidance import get_prompt
from .utils import parse_llm_response, validate_required_params

class CareerGuideAgent:
    def __init__(self):
        self.model = get_chat_model()
        self.prompt_template = get_prompt()

    def guide(self, user_query, profile_analysis_report, target_role):
        validate_required_params(
            user_query=user_query,
            profile_analysis_report=profile_analysis_report,
            target_role=target_role
        )
        try:
            prompt = self.prompt_template.format(
                user_query=user_query,
                profile_analysis_report=profile_analysis_report,
                target_role=target_role
            )
            response = self.model.invoke(prompt)
            return parse_llm_response(response)
        except Exception as e:
            raise ValueError(f"Failed to generate career guidance: {e}")
