# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory into the container
COPY . .

# Expose the port that Flask runs on
EXPOSE 5050

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5050"]
