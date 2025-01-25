from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch, F, OuterRef, Subquery, ExpressionWrapper, DurationField
from django.db.models.functions import Now
from django.utils import timezone
from django.utils.timezone import now, make_aware
from datetime import datetime, timedelta
from .models import User, Ride, RideEvent
from .serializers import RideSerializer, UserSerializer, RideEventSerializer
from .permissions import IsAdminUser
from .filters import RideFilter

import logging


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.prefetch_related(
        'id_rider',
        'id_driver',
        Prefetch(
            'ride_events',
            queryset=RideEvent.objects.filter(
                created_at__gte=make_aware(datetime(2022, 1, 1))
            ),
        ),
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
        email = self.request.query_params.get('email', None)
        sort_by_distance = self.request.query_params.get('sort_by_distance', None)

        logging.debug(f"Filtering rides with status: {status}, email: {email}, sort_by_distance: {sort_by_distance}")

        if status:
            queryset = queryset.filter(status=status)
        if email:
            queryset = queryset.filter(id_rider__email=email)

        if sort_by_distance:
            latitude = float(self.request.query_params.get('latitude', 0))
            longitude = float(self.request.query_params.get('longitude', 0))
            queryset = queryset.annotate(
                distance=ExpressionWrapper(
                    F('pickup_latitude') - latitude + F('pickup_longitude') - longitude,
                    output_field=FloatField()
                )
            ).order_by('distance')

        today = datetime.now().date()
        queryset = queryset.prefetch_related(
            Prefetch(
                'ride_events',
                queryset=RideEvent.objects.filter(
                    created_at__gte=today - timedelta(days=1)
                ),
                to_attr='todays_ride_events'
            )
        )

        logging.debug(f"Resulting queryset: {queryset.query}")

        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status
        new_status = request.data.get('status')

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if new_status and old_status != new_status:
            description = f"Status changed from {old_status} to {new_status}"
            RideEvent.objects.create(
                id_ride=instance,
                description=description
            )

        instance.refresh_from_db()

        return Response(serializer.data)



    @action(detail=False, methods=['get'])
    def trip_durations(self, request):
        queryset = self.get_queryset()
        pickup_events = RideEvent.objects.filter(
            id_ride=OuterRef('pk'),
            description='Status changed to pickup'
        ).order_by('created_at')
        dropoff_events = RideEvent.objects.filter(
            id_ride=OuterRef('pk'),
            description='Status changed to dropoff'
        ).order_by('created_at')

        queryset = queryset.annotate(
            pickup_event_time=Subquery(pickup_events.values('created_at')[:1]),
            dropoff_event_time=Subquery(dropoff_events.values('created_at')[:1]),
            trip_duration=ExpressionWrapper(
                F('dropoff_event_time') - F('pickup_event_time'),
                output_field=DurationField()
            )
        ).filter(trip_duration__gt=timedelta(hours=1))

        data = queryset.values('id_driver__username', 'trip_duration')
        return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id_user")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all().order_by("created_at")
    serializer_class = RideEventSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
