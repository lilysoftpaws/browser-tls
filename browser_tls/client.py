from playwright.async_api import async_playwright, Browser
from .context import BrowserContext
from .types import Headers, Method, RequestTimeoutError, Response
from .utils import (
    build_fetch_script,
    encode_body_and_headers,
    apply_query_params,
)
from typing import Optional, Dict, Any, Union

class BrowserClient:
    def __init__(self):
        self._playwright = None
        self._browser: Optional[Browser] = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()

    async def start(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=True,
            args=["--disable-web-security"]
        )

    async def stop(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    def new_context(self) -> BrowserContext:
        if not self._browser:
            raise RuntimeError("Browser not started")
        return BrowserContext(self._browser)

    async def request(
        self,
        url: str,
        method: Optional[Method] = None,
        headers: Optional[Headers] = None,
        data: Optional[Union[str, Dict[str, Any], list]] = None,
        params: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Response:
        full_url = apply_query_params(url, params)
        body, final_headers = encode_body_and_headers(data, headers)
        inferred_method = method or ("POST" if body else "GET")
        timeout_ms = int(timeout * 1000) if timeout else 0

        async with self.new_context() as context:
            script = build_fetch_script(full_url, inferred_method, final_headers, body, timeout_ms)
            result = await context.page.evaluate(script)

            if isinstance(result, dict) and result.get("error") == "AbortError":
                raise RequestTimeoutError(f"Request to {url} timed out after {timeout} seconds")

            return Response(
                status=result["status"],
                status_text=result["statusText"],
                headers=dict(result["headers"]),
                body=result["body"]
            )
