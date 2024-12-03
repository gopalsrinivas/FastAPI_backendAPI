import httpx
from app.config import config

async def get_location(ip: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{config.LOCATION_API_URL}/{ip}", params={"token": config.LOCATION_API_KEY})
            response.raise_for_status()
            data = response.json()

            if 'city' in data and 'country' in data:
                return {"city": data["city"], "country": data["country"]}
            else:
                raise Exception("Location data missing from the response")
    except Exception as e:
        return {"error": f"Failed to fetch location: {str(e)}"}
