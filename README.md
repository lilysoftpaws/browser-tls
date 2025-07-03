### browser-tls

Borrow fingerprints from real browsers

### Features

- Lightweight moderately featured API
- Send HTTP requests from within a real browser context

### Example

```python
import asyncio
from browser_tls import BrowserClient

async def main():
    async with BrowserClient() as client:
        response = await client.request("https://httpbin.org/get")
        print(response.status)
        print(response.json())

if __name__ == "__main__":
    asyncio.run(main())
```
