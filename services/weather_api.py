import aiohttp
from config import WEATHER_API_KEY

API_KEY = WEATHER_API_KEY


async def get_city_temperature(city_name: str):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": API_KEY, "units": "metric", "lang": "ru"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()

            if resp.status != 200:
                raise ValueError(data.get("message", "Ошибка запроса к OpenWeatherMap"))

            print(data)
            temp = data["main"]["temp"]
            print(temp)
            return temp
