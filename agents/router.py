__module_name__ = "router"

from backend.llm import get_chat_model
from backend.prompts.routing import get_prompt
from .utils import parse_llm_response, validate_required_params

class RoutingAgent:
    def __init__(self):
        self.model = get_chat_model()
        self.prompt_template = get_prompt()

    def route(self, state, conversation_history, user_input):
        validate_required_params(user_input=user_input)
        prompt = self.prompt_template.format(
            state=state,
            conversation_history=conversation_history,
            user_input=user_input
        )
        response = self.model.invoke(prompt)
        parsed_response = parse_llm_response(response)
        actions = {
            "CALL_ANALYZE", "CALL_REWRITE", "CALL_JOB_FIT", "CALL_GUIDE",
            "RESPOND_DIRECTLY", "AWAIT_URL", "AWAIT_CONFIRMATION",
            "REQUEST_JOB_DESCRIPTION", "INVALID_INPUT", "INITIAL_WELCOME"
        }
        if parsed_response.get('current_router_action') not in actions:
            parsed_response['current_router_action'] = 'RESPOND_DIRECTLY'
        return parsed_response
