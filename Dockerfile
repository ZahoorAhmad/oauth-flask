FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code into the container
COPY . /app/

# Set environment variable for Flask app
ENV FLASK_APP=app.app

# Expose the port
EXPOSE 5000

# Start Flask application
CMD ["python", "app/app.py"]
