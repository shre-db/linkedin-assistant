__module_name__ = "langgraph_graph"

from langgraph.graph import StateGraph, END, Graph
from .state_schema import ProfileBotState
from .handlers import analyze_node, rewrite_node, job_fit_node, guide_node, router_node
from backend.memory import get_memory_saver

def build_graph():
    graph = StateGraph(ProfileBotState)
    graph.add_node("Router", router_node)
    graph.add_node("AnalyzeProfile", analyze_node)
    graph.add_node("RewriteContent", rewrite_node)
    graph.add_node("EvaluateJobFit", job_fit_node)
    graph.add_node("CareerGuidance", guide_node)
    graph.set_entry_point("Router")

    def route_decision(state):
        return state.current_router_action

    graph.add_conditional_edges(
        "Router",
        route_decision,
        {
            "CALL_ANALYZE": "AnalyzeProfile",
            "CALL_REWRITE": "RewriteContent",
            "CALL_JOB_FIT": "EvaluateJobFit",
            "CALL_GUIDE": "CareerGuidance",
            "RESPOND_DIRECTLY": END,
            "AWAIT_URL": END,
            "AWAIT_CONFIRMATION": END,
            "REQUEST_JOB_DESCRIPTION": END,
            "INVALID_INPUT": END,
            "INITIAL_WELCOME": END,
        }
    )

    graph.add_edge("AnalyzeProfile", END)
    graph.add_edge("RewriteContent", END) 
    graph.add_edge("EvaluateJobFit", END)
    graph.add_edge("CareerGuidance", END)

    return graph

def get_graph_runner() -> Graph:
    raw_graph = build_graph()
    memory_instance = get_memory_saver()
    compiled_graph = raw_graph.compile(checkpointer=memory_instance)
    return compiled_graph
