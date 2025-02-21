FROM python:3.11-slim

# Install OS-level dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy everything, including the 'csv_files' folder
COPY . .
COPY csv_files /app/csv_files

# Expose port 5000 if needed
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
