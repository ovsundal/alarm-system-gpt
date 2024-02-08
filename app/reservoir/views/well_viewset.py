import json

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from reservoir.serializers.well_serializer import WellSerializer


class WellViewSet(GenericViewSet):
    lookup_field = 'name'

    def list(self, request):
        search_value = request.query_params.get(self.lookup_field, '')

        with open('reservoir/static_well_data.json', 'r') as f:
            static_well_data = json.load(f)

        filtered_data = [item for item in static_well_data
                         if search_value.lower()
                         in item[self.lookup_field].lower()]
        serializer = WellSerializer(filtered_data, many=True)

        return Response(serializer.data)
