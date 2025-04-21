# Use official Python image
FROM python:3.11.11-slim-bookworm


# Set working directory inside the container
WORKDIR /app

# Install OS packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

    
# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create data & logs folders inside the container
RUN mkdir -p logs data

# Expose Streamlit port
EXPOSE 8501

# Default command — you can override this in docker run

CMD ["streamlit", "run", "dashboard/app.py","--server.port=8501", "--server.address=0.0.0.0"]
