from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, UserViewSet, RideEventViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"rides", RideViewSet)
router.register(r"users", UserViewSet)
router.register(r"ride-events", RideEventViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "rides/trip_durations/",
        RideViewSet.as_view({"get": "trip_durations"}),
        name="trip-durations",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
