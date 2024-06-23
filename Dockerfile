# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory to the current directory
WORKDIR .

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]
