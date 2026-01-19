# Use stable Python version for Selenium compatibility
FROM python:3.10-slim

# Install system dependencies required by Chrome & Selenium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    unzip \
    curl \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libgbm1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver
ENV DISPLAY=:99

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire automation project
COPY . .

# Create folders used in your Base class
RUN mkdir -p Screenshots Downloads

# Default command: execute pytest with allure support
CMD ["pytest", "source_code/Login.py", "-v"]
