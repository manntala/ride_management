from rest_framework import serializers
from .models import User, Ride, RideEvent
from django.utils.timezone import now


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id_user", "role", "first_name", "last_name", "email", "phone_number"]


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ["id_ride_event", "id_ride", "description", "created_at"]


class RideSerializer(serializers.ModelSerializer):
    id_rider = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_driver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    ride_events = RideEventSerializer(many=True, read_only=True)
    todays_ride_events = serializers.SerializerMethodField()
    rider_username = serializers.SerializerMethodField()
    driver_username = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            "id_ride",
            "id_rider",
            "id_driver",
            "status",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "ride_events",
            "todays_ride_events",
            "rider_username",
            "driver_username",
            "distance",
        ]

    def get_todays_ride_events(self, obj):
        today = now().date()
        return RideEventSerializer(
            obj.ride_events.filter(created_at__date=today), many=True
        ).data

    def get_rider_username(self, obj):
        return obj.id_rider.username if obj.id_rider else None

    def get_driver_username(self, obj):
        return obj.id_driver.username if obj.id_driver else None

    def get_distance(self, obj):
        return getattr(obj, "distance", None)

    def create(self, validated_data):
        ride_events_data = validated_data.pop("ride_events", [])
        ride = Ride.objects.create(**validated_data)
        for ride_event_data in ride_events_data:
            RideEvent.objects.create(id_ride=ride, **ride_event_data)
        return ride
