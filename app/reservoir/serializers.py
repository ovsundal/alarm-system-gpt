from rest_framework import serializers
from reservoir.models import ReservoirMeasurement


class ReservoirMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservoirMeasurement
        fields = [
            'start_timestamp',
            'end_timestamp',
            'duration_hr',
            'reference_rate',
            'q',
            'p_26hr',
            't_26hr',
            'p_58hr',
            't_58hr',
            'wpi',
            'rpi',
            'cpi',
            'is_shutin',
            'is_prev_shutin',
            'pressure_std',
            'derivative_std',
        ]
