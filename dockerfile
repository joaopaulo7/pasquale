# Use an official lightweight Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Set host IP to run on
ENV PASQUALE_HOST="0.0.0.0"

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies without using cache to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the application
CMD ["python", "src/simple_server.py"]
