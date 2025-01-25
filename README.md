# Ride Management App

This is a simple ride management app built with Django and Docker.

## Features

- User management (Admin, Rider, Driver)
- Ride management
- Ride event tracking
- RESTful API with Django REST Framework
- JWT authentication
- Dockerized for easy deployment

## Requirements

- Docker
- Docker Compose

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/manntala/ride_management.git
cd ride_management

2. Build and run Docker containers
docker-compose up --build

3. Load initial data
docker-compose exec web python manage.py load_users
docker-compose exec web python manage.py load_rides

4. Access the application
http://localhost:8000

5. Running the Tests
docker-compose exec web python manage.py test

## API Endpoints

### Authentication

- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

### Users

- `GET /api/users/`: List all users
- `POST /api/users/`: Create a new user
- `GET /api/users/{id}/`: Retrieve a user
- `PUT /api/users/{id}/`: Update a user
- `DELETE /api/users/{id}/`: Delete a user

### Rides

- `GET /api/rides/`: List all rides
- `POST /api/rides/`: Create a new ride
- `GET /api/rides/{id}/`: Retrieve a ride
- `PUT /api/rides/{id}/`: Update a ride
- `DELETE /api/rides/{id}/`: Delete a ride

### Ride Events

- `GET /api/rideevents/`: List all ride events
- `POST /api/rideevents/`: Create a new ride event
- `GET /api/rideevents/{id}/`: Retrieve a ride event
- `PUT /api/rideevents/{id}/`: Update a ride event
- `DELETE /api/rideevents/{id}/`: Delete a ride event