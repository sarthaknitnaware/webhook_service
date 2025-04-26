FROM python:3.11-slim

WORKDIR /app

# Install any system dependencies
RUN apt-get update && apt-get install -y build-essential

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY entrypoint.sh .

# Expose FastAPI port
EXPOSE 8000

# Ensure our entrypoint is executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
