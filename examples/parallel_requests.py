import asyncio
from browser_tls import BrowserClient

async def fetch_example(client: BrowserClient, i: int):
    response = await client.request(
        url="https://httpbin.org/get",
        params={"id": str(i)}
    )
    print(i, response.status, response.json().get("args"))

async def main():
    async with BrowserClient() as client:
        tasks = [fetch_example(client, i) for i in range(100)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
