from rest_framework import serializers

from reservoir.models.reservoir_measurement import ReservoirMeasurement


class ReservoirMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservoirMeasurement
        fields = [
            'start_time',
            'reference_rate',
            'pressure',
            'temperature',
            'wpi',
            'rpi',
            'cpi',
        ]
