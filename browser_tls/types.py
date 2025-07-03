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


class FetchError(Exception):
    """Raised when fetch() encounters an error."""

    def __init__(self, url: str, js_message: str, js_stack: str):
        super().__init__(f"Failed to fetch {url!r}: {js_message}")
        self.url = url
        self.js_message = js_message
        self.js_stack = js_stack
