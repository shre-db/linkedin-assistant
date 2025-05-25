__module_name__ = "content_rewriter"

from backend.llm import get_chat_model
from backend.prompts.content_rewriting import get_prompt
from .utils import parse_llm_response, validate_required_params
from typing import Dict, Optional

class ContentRewriterAgent:
    def __init__(self):
        self.model = get_chat_model()
        self.prompt_template = get_prompt()

    def rewrite(self, current_content: dict, profile_analysis_report: dict, target_role: Optional[str] = None) -> Dict[str, any]:
        validate_required_params(
            current_content=current_content,
            profile_analysis_report=profile_analysis_report
        )
        prompt = self.prompt_template.format(
            current_linkedin_content=current_content,
            profile_analysis_report=profile_analysis_report,
            target_role=target_role or "the same role"
        )
        response = self.model.invoke(prompt)
        return parse_llm_response(response)
