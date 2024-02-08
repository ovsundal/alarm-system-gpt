from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservoir.views.reservoir_measurement_viewset import (
    ReservoirMeasurementViewSet)
from reservoir.views.well_viewset import WellViewSet

router = DefaultRouter()
router.register('WellMeasurements',
                ReservoirMeasurementViewSet)
router.register('Wells',
                WellViewSet, basename='Wells')

urlpatterns = [
    path('', include(router.urls)),
]
