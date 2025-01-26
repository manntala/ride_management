from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import (
    OuterRef,
    Subquery,
    ExpressionWrapper,
    F,
    DurationField,
    Prefetch,
)
from datetime import timedelta
from django.utils.timezone import now
from .models import User, Ride, RideEvent
from .serializers import RideSerializer, UserSerializer, RideEventSerializer
from .permissions import IsAdminUser
from .filters import RideFilter

import logging


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'pickup_time', 'status']
    ordering = ["pickup_time"]

    def get_queryset(self):
        queryset = Ride.objects.select_related(
            "id_rider", "id_driver"
        ).prefetch_related(
            Prefetch(
                "ride_events",
                queryset=RideEvent.objects.filter(
                    created_at__gte=now() - timedelta(days=1)
                ),
            )
        )

        status = self.request.query_params.get("status", None)
        email = self.request.query_params.get("email", None)
        sort_by_distance = self.request.query_params.get("sort_by_distance", None)

        logging.debug(
            f"Filtering rides with status: {status}, email: {email}, sort_by_distance: {sort_by_distance}"
        )

        if status:
            queryset = queryset.filter(status=status)
        if email:
            queryset = queryset.filter(id_rider__email=email)

        if sort_by_distance:
            try:
                latitude = float(self.request.query_params.get("latitude", 0))
                longitude = float(self.request.query_params.get("longitude", 0))
                user_location = Point(longitude, latitude, srid=4326)
                queryset = queryset.annotate(
                    distance=Distance(
                        Point(F('pickup_longitude'), F('pickup_latitude'), srid=4326), 
                        user_location
                    )
                ).order_by("distance")
            except (TypeError, ValueError) as e:
                logging.error(f"Invalid latitude or longitude values: {e}")

        logging.debug(f"Resulting queryset: {queryset.query}")
        return queryset

    def perform_create(self, serializer):
        ride = serializer.save()
        RideEvent.objects.create(id_ride=ride, description="Ride created")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status
        new_status = request.data.get("status")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if new_status and old_status != new_status:
            description = f"Status changed to {new_status}"
            RideEvent.objects.create(id_ride=instance, description=description)

            if new_status == "dropoff":
                instance.dropoff_time = now()  # Set the dropoff_time to the current time
                instance.distance = instance.pickup_location.distance(
                    instance.dropoff_location
                )
                instance.save()

        instance.refresh_from_db()

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def trip_durations(self, request):
        queryset = self.get_queryset()
        pickup_events = RideEvent.objects.filter(
            id_ride=OuterRef("pk"), description="Ride created"
        ).order_by("created_at")
        dropoff_events = RideEvent.objects.filter(
            id_ride=OuterRef("pk"), description="Status changed to dropoff"
        ).order_by("created_at")

        queryset = queryset.annotate(
            pickup_event_time=Subquery(pickup_events.values("created_at")[:1]),
            dropoff_event_time=Subquery(dropoff_events.values("created_at")[:1]),
            trip_duration=ExpressionWrapper(
                F("dropoff_event_time") - F("pickup_event_time"),
                output_field=DurationField(),
            ),
        ).filter(pickup_event_time__isnull=False, dropoff_event_time__isnull=False)

        data = queryset.values(
            "id_driver__username", "id_rider__username", "trip_duration"
        )
        return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id_user")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all().order_by("created_at")
    serializer_class = RideEventSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
