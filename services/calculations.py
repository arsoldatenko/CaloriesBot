from services.weather_api import get_city_temperature


async def calculated_water_norm(user_data):
    weight = user_data.get("weight")
    activity = user_data.get("activity")
    is_today_warm_p = await is_today_warm(user_data.get("city"))
    print(is_today_warm)
    if is_today_warm_p:
        return weight * 30 + 500 * int(activity / 30) + 750, "больше 20 градусов"
    else:
        return weight * 30 + 500 * int(activity / 30), "меньше 20 градусов"


async def calculated_calories_norm(user_data):
    weight = user_data.get("weight")
    height = user_data.get("height")
    age = user_data.get("age")
    gender = user_data.get("gender")
    activity = user_data.get("activity")
    koefficients = [1.2, 1.375, 1.55, 1.725, 1.9]
    if int(activity / 30) > 4:
        koefficient_number = 4
    else:
        koefficient_number = koefficients[int(activity / 30)]
    if gender == "male":
        return (weight * 10 + 6.25 * height - 5 * age + 5) * koefficient_number
    if gender == "female":
        return (weight * 10 + 6.25 * height - 5 * age - 161) * koefficient_number


async def is_today_warm(city):
    temp = await get_city_temperature(city)
    if temp > 20:
        return True
    else:
        return False
