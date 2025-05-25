__module_name__ = "memory"

from typing import Optional, Dict, Any
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver

_saver: Optional[BaseCheckpointSaver] = None

def get_memory_saver() -> BaseCheckpointSaver:
    global _saver
    if _saver is None:
        _saver = InMemorySaver()
    return _saver

def clear_memory() -> None:
    global _saver
    if _saver is not None:
        _saver = InMemorySaver()

def get_memory_stats() -> Dict[str, Any]:
    global _saver
    if _saver is None:
        return {"status": "not_initialized", "type": None}
    return {
        "status": "initialized",
        "type": type(_saver).__name__,
        "class": str(type(_saver))
    }
