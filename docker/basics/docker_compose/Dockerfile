# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Expose port 8000 to document which port the app uses
EXPOSE 8000

# Default command to run the app (will be overridden by Compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]