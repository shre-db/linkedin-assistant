__module_name__ = "handlers"

import json
from .state_schema import ProfileBotState, RouterAction
from agents.router import RoutingAgent
from agents.career_guide import CareerGuideAgent
from agents.content_rewriter import ContentRewriterAgent
from agents.job_fit_evaluator import JobFitEvaluatorAgent
from agents.profile_analyzer import ProfileAnalyzerAgent
from agents.utils import parse_llm_response

routing_agent = RoutingAgent()
analyzer = ProfileAnalyzerAgent()
rewriter = ContentRewriterAgent()
evaluator = JobFitEvaluatorAgent()
guide = CareerGuideAgent()

def router_node(state: ProfileBotState) -> ProfileBotState:
    current_user_input_for_turn = state.user_input
    history_before_llm_response = list(state.conversation_history)
    if current_user_input_for_turn and (
        not history_before_llm_response or 
        history_before_llm_response[-1].get("role") != "user" or 
        history_before_llm_response[-1].get("content") != current_user_input_for_turn
    ):
        state.conversation_history.append({"role": "user", "content": current_user_input_for_turn})
        history_before_llm_response = list(state.conversation_history)
    conversation_history_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history_before_llm_response])
    state_json = state.model_dump_json(indent=2)
    try:
        routing_response = routing_agent.route(
            state=state_json,
            conversation_history=conversation_history_str,
            user_input=current_user_input_for_turn
        )
        if isinstance(routing_response, dict):
            if "current_router_action" in routing_response:
                state.current_router_action = routing_response["current_router_action"]
            if "current_bot_response" in routing_response:
                state.current_bot_response = routing_response["current_bot_response"]
            if "linkedin_url" in routing_response and routing_response["linkedin_url"]:
                state.linkedin_url = routing_response["linkedin_url"]
            if "is_profile_analyzed" in routing_response:
                state.is_profile_analyzed = routing_response["is_profile_analyzed"]
            if "awaiting_user_confirmation" in routing_response:
                state.awaiting_user_confirmation = routing_response["awaiting_user_confirmation"]
            if "awaiting_job_description" in routing_response:
                state.awaiting_job_description = routing_response["awaiting_job_description"]
            if "proposed_next_action" in routing_response:
                state.proposed_next_action = routing_response["proposed_next_action"]
            if "last_agent_called" in routing_response:
                last_agent_value = routing_response["last_agent_called"]
                if last_agent_value == "null" or last_agent_value is None:
                    state.last_agent_called = None
                else:
                    state.last_agent_called = last_agent_value
        if (state.current_router_action == "CALL_JOB_FIT" and 
            current_user_input_for_turn and 
            not state.target_job_description):
            job_keywords = ["experience", "responsibilities", "qualifications", "requirements", 
                          "skills", "years", "education", "job summary", "salary", "benefits"]
            input_lower = current_user_input_for_turn.lower()
            keyword_count = sum(1 for keyword in job_keywords if keyword in input_lower)
            if keyword_count >= 3 or len(current_user_input_for_turn) > 200:
                state.target_job_description = current_user_input_for_turn
        if state.current_bot_response and (
            not state.conversation_history or
            state.conversation_history[-1].get("role") != "assistant" or
            state.conversation_history[-1].get("content") != state.current_bot_response
        ):
            state.conversation_history.append({"role": "assistant", "content": state.current_bot_response})
        return state
    except ValueError as e:
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        state.current_bot_response = "I apologize, I encountered an issue processing your request. Could you please rephrase?"
        state.error_message = f"Routing error: {str(e)}"
        state.conversation_history.append({"role": "assistant", "content": state.current_bot_response})
        return state
    except Exception as e:
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        state.current_bot_response = "I apologize, but I encountered an internal error. Please try again or rephrase your request."
        state.error_message = str(e)
        state.conversation_history.append({"role": "assistant", "content": state.current_bot_response})
        return state

def analyze_node(state: ProfileBotState) -> ProfileBotState:
    try:
        if not state.linkedin_data:
            error_msg = "No LinkedIn data available for analysis. Please provide a LinkedIn profile URL first."
            state.error_message = error_msg
            state.current_bot_response = error_msg
            state.current_router_action = RouterAction.AWAIT_URL
            return state
        result = analyzer.analyze(state.linkedin_data)
        state.profile_analysis_report = result
        state.is_profile_analyzed = True
        state.last_agent_called = "analyze"
        state.current_task_status = "Profile analysis completed"
        state.current_bot_response = "I've completed analyzing your LinkedIn profile. Would you like me to suggest content improvements or evaluate job fit?"
        return state
    except ValueError as e:
        state.error_message = f"Analysis error: {str(e)}"
        state.current_bot_response = "I encountered an issue analyzing your profile. Please ensure your LinkedIn data is valid."
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        return state
    except Exception as e:
        state.error_message = str(e)
        state.current_bot_response = "I apologize, but I encountered an error during profile analysis. Please try again."
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        return state

def rewrite_node(state: ProfileBotState) -> ProfileBotState:
    try:
        if not state.profile_analysis_report:
            error_msg = "Profile analysis required before content rewriting. Please analyze your profile first."
            state.error_message = error_msg
            state.current_bot_response = error_msg
            state.current_router_action = RouterAction.CALL_ANALYZE
            return state
        result = rewriter.rewrite(
            current_content=state.linkedin_data,
            profile_analysis_report=state.profile_analysis_report,
            target_role=state.target_role
        )
        state.content_rewrites_suggestions = result
        state.last_agent_called = "rewrite"
        state.current_task_status = "Content rewrite suggestions generated"
        state.current_bot_response = "I've generated optimized content suggestions for your LinkedIn profile. Would you like me to provide career guidance or evaluate job fit next?"
        return state
    except ValueError as e:
        state.error_message = f"Rewriting error: {str(e)}"
        state.current_bot_response = "I encountered an issue generating content suggestions. Please ensure your profile has been analyzed first."
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        return state
    except Exception as e:
        state.error_message = str(e)
        state.current_bot_response = "I apologize, but I encountered an error during content rewriting. Please try again."
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        return state

def job_fit_node(state: ProfileBotState) -> ProfileBotState:
    try:
        if not state.profile_analysis_report:
            error_msg = "Profile analysis required before job fit evaluation. Please analyze your profile first."
            state.error_message = error_msg
            state.current_bot_response = error_msg
            state.current_router_action = RouterAction.CALL_ANALYZE
            return state
        if not state.target_job_description:
            error_msg = "Job description required for fit evaluation. Please provide a job description."
            state.error_message = error_msg
            state.current_bot_response = error_msg
            state.current_router_action = RouterAction.REQUEST_JOB_DESCRIPTION
            state.awaiting_job_description = True
            return state
        result = evaluator.evaluate_fit(
            profile_analysis_report=state.profile_analysis_report,
            job_description=state.target_job_description
        )
        state.job_fit_evaluation_report = result
        state.last_agent_called = "job_fit"
        state.current_task_status = "Job fit evaluation completed"
        state.awaiting_job_description = False
        state.current_bot_response = "I've completed the job fit evaluation. Would you like career guidance based on these results?"
        return state
    except ValueError as e:
        state.error_message = f"Job fit error: {str(e)}"
        state.current_bot_response = "I encountered an issue evaluating job fit. Please ensure both profile analysis and job description are available."
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        return state
    except Exception as e:
        state.error_message = str(e)
        state.current_bot_response = "I apologize, but I encountered an error during job fit evaluation. Please try again."
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        return state

def guide_node(state: ProfileBotState) -> ProfileBotState:
    try:
        if not state.user_input:
            error_msg = "User query required for career guidance. Please ask a specific career question."
            state.error_message = error_msg
            state.current_bot_response = error_msg
            state.current_router_action = RouterAction.RESPOND_DIRECTLY
            return state
        result = guide.guide(
            user_query=state.user_input,
            profile_analysis_report=state.profile_analysis_report or {},
            target_role=state.target_role or "your desired role"
        )
        state.career_guidance_notes = result
        state.last_agent_called = "guide"
        state.current_task_status = "Career guidance provided"
        state.current_bot_response = "I've provided personalized career guidance. Is there anything specific you'd like to explore further?"
        return state
    except ValueError as e:
        state.error_message = f"Career guidance error: {str(e)}"
        state.current_bot_response = "I encountered an issue providing career guidance. Please ask a specific career-related question."
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        return state
    except Exception as e:
        state.error_message = str(e)
        state.current_bot_response = "I apologize, but I encountered an error providing career guidance. Please try again."
        state.current_router_action = RouterAction.RESPOND_DIRECTLY
        return state
