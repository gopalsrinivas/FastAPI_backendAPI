import logging
from fastapi import APIRouter, Request, HTTPException
from app.services.location_service import get_location
from app.services.weather_service import get_weather
from app.utils.cache import cache
from app.utils.validators import validate_ip
from app.utils.rate_limiter import rate_limiter

router = APIRouter()

logger = logging.getLogger("weather_api")


@router.get("/weather-by-ip")
@rate_limiter
async def weather_by_ip(request: Request = None, ip: str = None):
    ip = ip or request.client.host

    # Validate the IP address
    if not validate_ip(ip):
        raise HTTPException(status_code=400, detail="Invalid IP address")

    # Get location based on the IP address
    location = await get_location(ip)
    if "error" in location:
        raise HTTPException(status_code=502, detail=location["error"])

    # Get weather information from the location
    city = location["city"]
    cached_weather = cache.get(city)
    if cached_weather:
        return cached_weather

    weather = await get_weather(city)
    if "error" in weather:
        raise HTTPException(status_code=502, detail=weather["error"])

    response = {
        "ip": ip,
        "location": location,
        "weather": weather
    }
    cache.set(city, response)
    return response
