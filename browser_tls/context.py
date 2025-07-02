from playwright.async_api import Browser, BrowserContext as PWBrowserContext, Page
from typing import Optional

class BrowserContext:
    def __init__(self, browser: Browser):
        self._browser = browser
        self._context: Optional[PWBrowserContext] = None
        self._page: Optional[Page] = None

    async def __aenter__(self):
        self._context = await self._browser.new_context()
        self._page = await self._context.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._context:
            await self._context.close()

    @property
    def page(self) -> Page:
        if not self._page:
            raise RuntimeError("Page not initialized")
        return self._page
