import json
from urllib.parse import urlencode
from typing import Optional, Dict, Any


def build_fetch_script(
    url: str,
    method: str,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    timeout_ms: Optional[int] = None,
) -> str:
    fetch_options = {"method": method, "headers": headers or {}}
    if body:
        fetch_options["body"] = body

    fetch_script = f"""
    (() => {{
        const controller = new AbortController();
        const signal = controller.signal;
        const timeout = {timeout_ms} || 0;
        if (timeout > 0) {{
            setTimeout(() => controller.abort(), timeout);
        }}

        return fetch({json.dumps(url)}, {{
            ...{json.dumps(fetch_options)},
            signal
        }})
        .then(resp => resp.text().then(text => {{
            return {{
                status: resp.status,
                statusText: resp.statusText,
                headers: Array.from(resp.headers.entries()),
                body: text
            }};
        }}))
        .catch(err => {{
            return {{
                error: err.name,
                message: err.message,
                stack: err.stack
            }};
        }});
    }})()
    """
    return fetch_script


def encode_body_and_headers(
    data: Optional[Any], headers: Optional[Dict[str, str]]
) -> tuple[Optional[str], Dict[str, str]]:
    final_headers = headers.copy() if headers else {}

    if data is None:
        return None, final_headers

    if isinstance(data, (dict, list)):
        final_headers.setdefault("Content-Type", "application/json")
        return json.dumps(data), final_headers
    elif isinstance(data, str):
        return data, final_headers
    else:
        raise TypeError("Unsupported data type for body: must be dict, list, or str")


def apply_query_params(url: str, params: Optional[Dict[str, str]]) -> str:
    if not params:
        return url
    return f"{url}?{urlencode(params)}"
