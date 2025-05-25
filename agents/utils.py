__module_name__ = "utils"

import json

def parse_llm_response(response):
    try:
        if hasattr(response, "content"):
            response = response.content
        if not isinstance(response, str):
            response = str(response)
        if isinstance(response, dict):
            return response
        response = response.strip()
        if response.startswith("```json"):
            json_start = response.find("```json") + len("```json")
            json_end = response.rfind("```")
            if json_end > json_start:
                json_content = response[json_start:json_end].strip()
            else:
                json_content = response[json_start:].strip()
        elif response.startswith("```") and "json" in response[:20]:
            lines = response.split('\n')
            start_line = 1
            while start_line < len(lines) and lines[start_line].strip() == "":
                start_line += 1
            end_line = len(lines) - 1
            while end_line > start_line and (lines[end_line].strip() == "" or lines[end_line].strip() == "```"):
                end_line -= 1
            json_content = '\n'.join(lines[start_line:end_line + 1])
        else:
            json_content = response
        return json.loads(json_content)
    except Exception:
        raise ValueError("Invalid JSON response from LLM")

def validate_required_params(**kwargs):
    for param_name, param_value in kwargs.items():
        if param_value is None:
            raise ValueError(f"Required parameter '{param_name}' cannot be None")
        if isinstance(param_value, str) and not param_value.strip():
            raise ValueError(f"Required parameter '{param_name}' cannot be empty")
        if isinstance(param_value, dict) and not param_value:
            raise ValueError(f"Required parameter '{param_name}' cannot be empty")
