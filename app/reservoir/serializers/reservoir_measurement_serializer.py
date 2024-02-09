from rest_framework import serializers

from reservoir.models.reservoir_measurement import ReservoirMeasurement


class ReservoirMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservoirMeasurement
        fields = [
            'start_timestamp',
            'end_timestamp',
            'duration_hr',
            'reference_rate',
            'q',
            'P_26hr',
            'T_26hr',
            'P_58hr',
            'T_58hr',
            'wpi',
            'rpi',
            'cpi',
            'is_shutin',
            'is_prev_shutin',
            'time_from_shutin',
            'pressure_std',
            'derivative_std',
            'well_id'
        ]
