# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama
RUN pip install ollama

# Expose port (if needed)
EXPOSE 8080

# Run deepseek-r1:7b
CMD ["ollama", "run", "deepseek-r1:7b"]