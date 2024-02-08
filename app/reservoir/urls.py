from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservoir.views import ReservoirMeasurementViewSet

router = DefaultRouter()
router.register('WellReservoirMeasurements',
                ReservoirMeasurementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
