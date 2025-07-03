from typing import Any, Dict, Optional, Union, Literal
from dataclasses import dataclass
import json

Headers = Dict[str, str]
JSONType = Union[Dict[str, Any], list]
Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]


@dataclass
class Response:
    status: int
    status_text: str
    headers: Dict[str, str]
    body: str

    def json(self) -> Any:
        try:
            return json.loads(self.body)
        except json.JSONDecodeError as ex:
            raise ValueError("Response body is not valid JSON") from ex


class RequestTimeoutError(Exception):
    """Raised when a browser request times out."""
    pass
