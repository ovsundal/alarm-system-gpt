import json

from rest_framework.mixins import (
    RetrieveModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from reservoir.models.reservoir_measurement import ReservoirMeasurement
from reservoir.serializers.reservoir_measurement_serializer import (
    ReservoirMeasurementSerializer)
from reservoir.services.reservoir_measurement_services import (
    filter_reservoir_data)


class ReservoirMeasurementViewSet(
    GenericViewSet,  # generic view functionality
    RetrieveModelMixin,  # handles GETs for 1 Company
):
    serializer_class = ReservoirMeasurementSerializer
    queryset = ReservoirMeasurement.objects.all()
    lookup_field = 'well_id'

    def retrieve(self, request, *args, **kwargs):
        well_id = kwargs.get(self.lookup_field)

        with open('reservoir/data/static_reservoir_data.json', 'r') as f:
            static_reservoir_data = json.load(f)

        filtered_data = [item for item in static_reservoir_data
                         if item[self.lookup_field] == int(well_id)]

        if len(filtered_data) == 0:
            return Response([])

        processed_data = filter_reservoir_data(filtered_data)

        return Response(processed_data)
