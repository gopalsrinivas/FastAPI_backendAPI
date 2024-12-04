from httpx import AsyncClient, HTTPStatusError, RequestError
import logging
from app.config import config
import asyncio

logger = logging.getLogger(__name__)

async def get_location(ip: str):
    max_retries = 3
    delay = 2
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempt {attempt+1} to fetch location for IP: {ip}")
            async with AsyncClient() as client:
                response = await client.get(f"{config.LOCATION_API_URL}/{ip}", params={"token": config.LOCATION_API_KEY})
                response.raise_for_status()
                data = response.json()

                if 'city' in data and 'country' in data:
                    logger.info(f"Location found for {ip}: {data['city']}, {data['country']}")
                    return {"city": data["city"], "country": data["country"]}
                else:
                    logger.warning(f"Incomplete location data for {ip}")
                    raise ValueError("Incomplete location data")
        except (HTTPStatusError, RequestError) as e:
            if attempt < max_retries - 1:
                logger.warning(f"Retrying due to error: {str(e)}")
                await asyncio.sleep(delay)
            else:
                logger.error(f"Failed to fetch location for IP {ip}: {str(e)}")
                return {"error": f"Failed to fetch location: {str(e)}"}
