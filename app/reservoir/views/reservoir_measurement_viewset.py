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
    filter_reservoir_data,
    add_alarm_limits_to_reservoir_data,
    round_numbers, calculate_trend_lines
)


class ReservoirMeasurementViewSet(
    GenericViewSet,
    RetrieveModelMixin,
):
    serializer_class = ReservoirMeasurementSerializer
    queryset = ReservoirMeasurement.objects.all()
    lookup_field = 'well_id'

    def retrieve(self, request, *args, **kwargs):
        well_id = kwargs.get(self.lookup_field)
        print(request)
        alarm_lower_limit = request.query_params.get('lowerAlarm')
        alarm_upper_limit = request.query_params.get('upperAlarm')

        with open('reservoir/data/static_reservoir_data.json', 'r') as f:
            static_reservoir_data = json.load(f)

        filtered_data = [item for item in static_reservoir_data
                         if item[self.lookup_field] == int(well_id)]

        if len(filtered_data) == 0:
            return Response([])

        filtered_sorted_data = sorted(filtered_data,
                                      key=lambda x: x['start_time']
                                      )

        processed_data = filter_reservoir_data(filtered_sorted_data)
        processed_data = add_alarm_limits_to_reservoir_data(
            processed_data, alarm_lower_limit, alarm_upper_limit)
        processed_data = round_numbers(processed_data)
        processed_data = calculate_trend_lines(processed_data)

        return Response(processed_data)
