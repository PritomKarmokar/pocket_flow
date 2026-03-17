# Python Imports
from typing import Any, Dict

def format_output_success(response: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    if data:
        response['data'] = data
    return response

def format_output_error(response: Dict[str, Any], error: str) -> Dict[str, Any]:
    if error:
        response['error'] = error
    return response