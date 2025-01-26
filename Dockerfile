FROM python:3.11-slim

# Install GDAL dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && apt-get clean

# Set GDAL_LIBRARY_PATH environment variable
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app
WORKDIR /app

# Run the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]