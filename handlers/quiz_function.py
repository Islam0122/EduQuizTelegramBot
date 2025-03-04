import aiohttp


async def get_topics():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://eduquiz-back-end.onrender.com/api/v1/topics/") as response:
            return await response.json()

