from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Ride, RideEvent
from datetime import datetime
from django.utils.timezone import make_aware

User = get_user_model()


class RideViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            role="admin",
        )
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.driver = User.objects.create_user(
            username="driveruser",
            email="driveruser@example.com",
            password="driverpass",
            role="driver",
        )
        self.ride = Ride.objects.create(
            id_rider=self.user,
            id_driver=self.driver,
            pickup_time=make_aware(datetime(2023, 1, 1)),
            pickup_latitude=10.0,
            pickup_longitude=10.0,
            dropoff_latitude=20.0,
            dropoff_longitude=20.0,
            status="pickup",
        )
        self.ride_event = RideEvent.objects.create(
            id_ride=self.ride,
            description="Pickup event",
            created_at=make_aware(datetime(2023, 1, 1)),
        )

    def test_ride_viewset_list(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("ride-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ride_viewset_filter_by_status(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("ride-list")
        response = self.client.get(url, {"status": "pickup"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "pickup")
        self.assertEqual(results[0]["id_rider"], self.user.id_user)
        self.assertEqual(results[0]["id_driver"], self.driver.id_user)

    def test_user_viewset_list(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
