FROM python:3.11-slim

WORKDIR /app

# Install any system dependencies
RUN apt-get update && apt-get install -y build-essential netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY entrypoint.sh .

COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Expose FastAPI port
EXPOSE 8000

# Ensure our entrypoint is executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
