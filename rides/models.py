from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.geos import Point


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("rider", "Rider"),
        ("driver", "Driver"),
    )
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.email}"


class Ride(models.Model):
    STATUS_CHOICES = (
        ("en-route", "En-route"),
        ("pickup", "Pickup"),
        ("dropoff", "Dropoff"),
    )
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    id_rider = models.ForeignKey(
        User, related_name="rides_as_rider", on_delete=models.CASCADE
    )
    id_driver = models.ForeignKey(
        User, related_name="rides_as_driver", on_delete=models.CASCADE
    )
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()
    dropoff_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pickup_latitude and self.pickup_longitude:
            self.pickup_location = Point(self.pickup_longitude, self.pickup_latitude)
        if self.dropoff_latitude and self.dropoff_longitude:
            self.dropoff_location = Point(self.dropoff_longitude, self.dropoff_latitude)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_rider.email}"


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(
        Ride, related_name="ride_events", on_delete=models.CASCADE
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.id_ride.id_rider.email}"
