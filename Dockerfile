FROM python:3.11-slim

# Prevents Python from writing .pyc files & buffering logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    unzip \
    zip \
    p7zip-full \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Healthcheck (optional - good for Koyeb/Render/Heroku)
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python3 -c "import socket; s=socket.socket(); s.connect(('127.0.0.1', 80))" || exit 1

# Run bot (main.py is entrypoint)
CMD ["python3", "main.py"]
