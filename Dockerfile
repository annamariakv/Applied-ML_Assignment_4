# Start from a Python 3 base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY app.py .
COPY score.py .
COPY trained_model.joblib .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Command to run on container start
CMD ["python", "app.py"]
