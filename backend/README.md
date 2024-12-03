# Weather API Backend

## **Overview**
A RESTful API to fetch weather details based on a user's IP address. Features include caching, rate limiting, proper error handling, and integration with location and weather services.

---

## **Features**
- **Fetch Weather**: Retrieves city and country using IP and fetches the current weather details.
- **Caching**: Weather data is cached for 10 minutes to optimize API calls.
- **Rate Limiting**: Limits each client IP to 5 requests per minute.
- **Error Handling**: Graceful responses for invalid inputs and external API failures.
- **Secure Configurations**: API keys are stored securely using `.env`.

---

## **Setup**

### Prerequisites
- Docker & Docker Compose installed
- Python 3.9+ installed (for local testing)

### Environment Variables
Add the following to a `.env` file in the `backend` directory:
```env
LOCATION_API_KEY=your_location_api_key
WEATHER_API_KEY=your_weather_api_key

### Docker runing

docker build -t weather-api .
docker run -p 8000:8000 weather-api
