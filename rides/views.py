from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Prefetch, F
from django.utils.timezone import now
from django.utils.timezone import make_aware
from datetime import datetime
from .models import User, Ride, RideEvent
from .serializers import RideSerializer, UserSerializer, RideEventSerializer
from .permissions import IsAdminUser
from .filters import RideFilter

import logging

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.prefetch_related(
        'id_rider',
        'id_driver',
        Prefetch('ride_events', queryset=RideEvent.objects.filter(created_at__gte=make_aware(datetime(2022, 1, 1))))
    ).all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time', 'pickup_latitude', 'pickup_longitude']
    ordering = ['pickup_time']

    def get_queryset(self):
        queryset = self.queryset
        status = self.request.query_params.get('status', None)
        email = self.request.query_params.get('rider_email', None)
        sort_by_distance = self.request.query_params.get('sort_by_distance', None)

        logging.debug(f"Filtering rides with status: {status}, email: {email}, sort_by_distance: {sort_by_distance}")

        if status:
            queryset = queryset.filter(status=status)
        if email:
            queryset = queryset.filter(id_rider__email=email)

        # Sorting by pickup_time or distance to pickup point
        if sort_by_distance:
            latitude = float(self.request.query_params.get('latitude', 0))
            longitude = float(self.request.query_params.get('longitude', 0))
            queryset = queryset.annotate(
                distance=F('pickup_latitude') - latitude + F('pickup_longitude') - longitude
            ).order_by('distance')

        logging.debug(f"Resulting queryset: {queryset.query}")

        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
