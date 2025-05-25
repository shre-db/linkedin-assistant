__module_name__ = "job_fit_evaluator"

from backend.llm import get_chat_model
from backend.prompts.job_fit import get_prompt
from .utils import parse_llm_response, validate_required_params

class JobFitEvaluatorAgent:
    def __init__(self):
        self.model = get_chat_model()
        self.prompt_template = get_prompt()

    def evaluate_fit(self, profile_analysis_report, job_description):
        validate_required_params(
            profile_analysis_report=profile_analysis_report,
            job_description=job_description
        )
        prompt = self.prompt_template.format(
            profile_analysis_report=profile_analysis_report,
            target_job_description=job_description
        )
        response = self.model.invoke(prompt)
        return parse_llm_response(response)
