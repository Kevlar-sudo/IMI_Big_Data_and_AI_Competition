FROM python:3.11-slim

# Install OS-level dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libssl-dev \
    libffi-dev \
    # For lxml
    libxml2-dev \
    libxslt-dev \
    # For opencv (headless)
    libgl1 \
    libglib2.0-0 \
    # Potentially more libs for other packages
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
