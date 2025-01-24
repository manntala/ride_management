from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rides.views import RideViewSet, UserViewSet, RideEventViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet)
router.register(r'users', UserViewSet)
router.register(r'ride-events', RideEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
