from fastapi import APIRouter, HTTPException, Query, Request
from app.services.location_service import get_location
from app.services.weather_service import get_weather
from app.utils.validators import validate_ip

router = APIRouter()


@router.get("/weather-by-ip")
async def weather_by_ip(
    ip: str = Query(..., description="The IP address to fetch weather for")
):
    """
    Fetch weather details using an IP address.
    """
    # Validate the IP address
    if not validate_ip(ip):
        raise HTTPException(
            status_code=400, detail="Invalid IP address format")

    # Fetch location data
    location = await get_location(ip)
    if "error" in location:
        raise HTTPException(status_code=502, detail=location["error"])

    # Fetch weather data
    city = location.get("city", "Unknown")
    weather = await get_weather(city)
    if "error" in weather:
        raise HTTPException(status_code=502, detail=weather["error"])

    return {
        "ip": ip,
        "location": location,
        "weather": weather
    }
