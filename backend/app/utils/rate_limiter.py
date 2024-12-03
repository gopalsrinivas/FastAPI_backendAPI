from fastapi import HTTPException, Request
from time import time
from app.config import config

rate_limiters = {}


def rate_limiter(func):
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        client_ip = request.client.host
        now = time()

        if client_ip not in rate_limiters:
            rate_limiters[client_ip] = [now]
        else:
            rate_limiters[client_ip] = [
                t for t in rate_limiters[client_ip] if t > now - 60]
            if len(rate_limiters[client_ip]) >= config.RATE_LIMIT:
                raise HTTPException(
                    status_code=429, detail="Rate limit exceeded")
            rate_limiters[client_ip].append(now)

        return await func(*args, **kwargs)
    return wrapper
