# views.py
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from reservoir.models import ReservoirMeasurement
from reservoir.serializers import ReservoirMeasurementSerializer
import json

from reservoir.services import process_reservoir_data


class ReservoirMeasurementViewSet(GenericViewSet,  # generic view functionality
                                  # CreateModelMixin,  # handles POSTs
                                  RetrieveModelMixin,  # handles GETs for 1 Company
                                  # UpdateModelMixin,  # handles PUTs and PATCHes
                                  # ListModelMixin      # handles GETs for many Companies
                                  ):
    serializer_class = ReservoirMeasurementSerializer
    queryset = ReservoirMeasurement.objects.all()
    lookup_field = 'well_id'

    def retrieve(self, request, *args, **kwargs):
        print(kwargs)
        well_id = kwargs.get('well_id')

        with open('reservoir/static_reservoir_data.json', 'r') as f:
            static_reservoir_data = json.load(f)

        data = static_reservoir_data.get(well_id)
        processed_data = process_reservoir_data(data)

        if data is None:
            return Response({"message": "Data not found"}, status=404)

        return Response(data)
