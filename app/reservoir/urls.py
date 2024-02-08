from django.urls import path, include, register_converter
from rest_framework.routers import DefaultRouter

from reservoir.views import ReservoirMeasurementViewSet

router = DefaultRouter()
router.register('WellReservoirMeasurements', ReservoirMeasurementViewSet, basename='reservoir_measurement')

urlpatterns = [
    path('', include(router.urls)),
]
