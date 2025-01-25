# Use the official Python image from the Docker Hub
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Run the Django development server with migrations
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]