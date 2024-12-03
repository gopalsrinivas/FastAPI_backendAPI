import logging
from fastapi import FastAPI
from app.api.weather import router as weather_router
from fastapi import Request

app = FastAPI()

# Include the weather router
app.include_router(weather_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to Weather API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


logging.basicConfig(level=logging.INFO)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("app")
    logger.info(f"Request URL: {request.url}")
    response = await call_next(request)
    logger.info(f"Response Status: {response.status_code}")
    return response


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("app")
    routes = [route.path for route in app.routes]
    logger.info(f"Registered routes: {routes}")
