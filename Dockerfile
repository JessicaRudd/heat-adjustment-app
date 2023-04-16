# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the app files
COPY app.py .
COPY heat_index_pace_adjustment.py .
COPY weather_data.py .
COPY templates templates/

# Set environment variables
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Expose the port
EXPOSE 5000

# Start the app
CMD ["flask", "run", "--host", "0.0.0.0"]
