<div>
  <strong>browser-tls</strong><br>
  <p style="margin-top: 0;">borrow the fingerprints of real browsers</p>
</div>

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
