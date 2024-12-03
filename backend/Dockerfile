FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only requirements.txt to leverage Docker cache efficiently
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Command to run your FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
