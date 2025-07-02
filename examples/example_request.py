import asyncio
from browser_tls import BrowserClient

async def main():
    async with BrowserClient() as client:
        response = await client.request(
            url="https://httpbin.org/post",
            data={ "id": 0 }
        )
        print(response.status, response.headers, response.body)

if __name__ == "__main__":
    asyncio.run(main())
