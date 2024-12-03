import httpx
from app.config import config


async def get_weather(city: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(config.WEATHER_API_URL, params={"q": city, "appid": config.WEATHER_API_KEY, "units": "metric"})
            response.raise_for_status()
            data = response.json()

            if 'main' in data and 'weather' in data:
                return {
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"]
                }
            else:
                raise Exception("Weather data missing from the response")
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}
