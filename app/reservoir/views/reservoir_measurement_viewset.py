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
    round_numbers, extend_timelines,
    calculate_and_add_slope_intercept_and_r_squared_for_benchmark
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
        rpi_alarm_lower_limit = request.query_params.get('rpiLowerAlarm')
        rpi_alarm_upper_limit = request.query_params.get('rpiUpperAlarm')
        cpi_alarm_lower_limit = request.query_params.get('cpiLowerAlarm')
        cpi_alarm_upper_limit = request.query_params.get('cpiUpperAlarm')
        wpi_alarm_lower_limit = request.query_params.get('wpiLowerAlarm')
        wpi_alarm_upper_limit = request.query_params.get('wpiUpperAlarm')

        alarms_list = [rpi_alarm_lower_limit, rpi_alarm_upper_limit,
                       cpi_alarm_lower_limit, cpi_alarm_upper_limit,
                       wpi_alarm_lower_limit, wpi_alarm_upper_limit]

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
            processed_data, alarms_list)
        processed_data = calculate_and_add_slope_intercept_and_r_squared_for_benchmark(processed_data)
        processed_data = round_numbers(processed_data)

        future_years_to_extend = 1
        for i in range(future_years_to_extend):
            processed_data = extend_timelines(processed_data)

        return Response(processed_data)
