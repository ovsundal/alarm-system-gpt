from rest_framework import serializers
from reservoir.models.well import Well


class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = ['id', 'name']
