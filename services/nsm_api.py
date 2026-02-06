import aiohttp


async def search_city(query: str):
    url = "https://nominatim.openstreetmap.org/search"

    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "MyFitnessBot/1.0 (harris.thom321@gmail.com)"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            data = await response.json()

            if response.status != 200:
                print("Ошибка запроса в API городов")
                return None

    return data
