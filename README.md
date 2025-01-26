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
docker-compose exec web python manage.py load_rides # as needed but not important

4. Access the application
http://localhost:8000

5. Running the Tests/Unit tests
docker-compose exec web python manage.py test

## API Endpoints

### Authentication

- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

Sample Payload:
{
    "username": "manny_talaroc",
    "password": 1234
}

### Users

- `GET /api/users/`: List all users
- `POST /api/users/`: Create a new user
- `GET /api/users/{id}/`: Retrieve a user
- `PUT /api/users/{id}/`: Update a user
- `DELETE /api/users/{id}/`: Delete a user

Sample Payload:
{
    "role": "admin",
    "first_name": "manny",
    "last_name": "talaroc",
    "email": "manny.talaroc@email.com",
    "phone_number": "121212"
}

### Rides

- `GET /api/rides/`: List all rides
- `POST /api/rides/`: Create a new ride
- `GET /api/rides/{id}/`: Retrieve a ride
- `PUT /api/rides/{id}/`: Update a ride
- `DELETE /api/rides/{id}/`: Delete a ride

Sample Payload:
{
    "id_rider": 1,
    "id_driver": 2,
    "pickup_time": "2023-10-10T10:00:00Z",
    "pickup_latitude": 37.7749,
    "pickup_longitude": -122.4194,
    "dropoff_latitude": 37.7849,
    "dropoff_longitude": -122.4294,
    "status": "en-route",
    "ride_events": [
        {
            "event_type": "pickup",
            "created_at": "2023-10-10T10:05:00Z",
            "description": "Rider picked up"
        },
        {
            "event_type": "dropoff",
            "created_at": "2023-10-10T10:30:00Z",
            "description": "Rider dropped off"
        }
    ]
}

### Ride Events

- `GET /api/ride-events/`: List all ride events
- `POST /api/ride-events/`: Create a new ride event
- `GET /api/ride-events/{id}/`: Retrieve a ride event
- `PUT /api/ride-events/{id}/`: Update a ride event
- `DELETE /api/ride-events/{id}/`: Delete a ride event

Sample Payload:
{
    "id_ride_event": 4,
    "id_ride": 2,
    "description": "Jane Smith Pickup test",
    "created_at": "2025-01-25T13:27:34.467373Z"
}


### SQL Query:
NOTE! 
psql should be installed first!
For WSL2: sudo apt install postgresql-client

Command to access
docker exec -it ride_management-db-1 psql -U user -d ride_management

## Reporting

### Trips Longer Than 1 Hour by Month and Driver

To generate a report of trips that took more than 1 hour from pickup to dropoff, grouped by month and driver, use the following SQL query:

```sql
SELECT 
    TO_CHAR(pickup_time, 'YYYY-MM') AS month,
    d.email AS driver,
    COUNT(*) AS count_of_trips
FROM 
    rides_ride r
JOIN 
    rides_user d ON r.id_driver_id = d.id_user
WHERE 
    EXTRACT(EPOCH FROM (r.dropoff_time - r.pickup_time)) > 3600
GROUP BY 
    TO_CHAR(pickup_time, 'YYYY-MM'), d.email
ORDER BY 
    month, driver;