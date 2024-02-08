import json

from rest_framework.mixins import (
    RetrieveModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from reservoir.models import ReservoirMeasurement
from reservoir.serializers import ReservoirMeasurementSerializer
from reservoir.services import process_reservoir_data


class ReservoirMeasurementViewSet(
    GenericViewSet,  # generic view functionality
    # CreateModelMixin,  # handles POSTs
    RetrieveModelMixin,  # handles GETs for 1 Company
    # UpdateModelMixin,  # handles PUTs and PATCHes
    # ListModelMixin      # handles GETs for many Companies
):
    serializer_class = ReservoirMeasurementSerializer
    queryset = ReservoirMeasurement.objects.all()
    lookup_field = 'well_id'

    def retrieve(self, request, *args, **kwargs):
        well_id = kwargs.get('well_id')

        with open('reservoir/static_reservoir_data.json', 'r') as f:
            static_reservoir_data = json.load(f)

        data = static_reservoir_data.get(well_id)
        if data is None:
            return Response({"message": "Data not found"}, status=404)

        processed_data = process_reservoir_data(data)

        return Response(processed_data)
