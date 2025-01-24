from rest_framework import serializers
from .models import User, Ride, RideEvent
from django.utils.timezone import now, timedelta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'role', 'first_name', 'last_name', 'email', 'phone_number']

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'description', 'created_at']

class RideSerializer(serializers.ModelSerializer):
    id_rider = UserSerializer()
    id_driver = UserSerializer()
    ride_events = RideEventSerializer(many=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = ['id_ride', 'id_rider', 'id_driver', 'status', 'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'pickup_time', 'ride_events', 'todays_ride_events']

    def get_todays_ride_events(self, obj):
        today = now().date()
        return RideEventSerializer(obj.ride_events.filter(created_at__date=today), many=True).data
