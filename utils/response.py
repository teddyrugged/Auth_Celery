# def build_response(flag: bool, message: str, result=None):
#     return {
#         "flag": flag,
#         "message": message,
#         "result": result,
#     }



# utils/response.py
from typing import Any, Optional, Dict, Union

def build_response(
    flag: bool,
    message: str,
    result: Optional[Union[Dict[str, Any], list, str, None]] = None
) -> Dict[str, Any]:
    return {
        "flag": flag,
        "message": message,
        "result": result,
    }
