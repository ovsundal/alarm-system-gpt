import urllib

from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from chat.models.chat_model import Chat
from chat.serializers.chat_serializer import ChatSerializer
from chat.services.services.chat_services import ask_openai, extract_data_from_llm_response


class ChatViewSet(GenericViewSet, CreateModelMixin):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        user_prompt = request.data.get('user_prompt')
        rpi_alarms = request.data.get('rpiAlarmValues')
        cpi_alarms = request.data.get('cpiAlarmValues')
        wpi_alarms = request.data.get('wpiAlarmValues')
        encoded_user_prompt = urllib.parse.quote(user_prompt)

        llm_response = ask_openai(encoded_user_prompt)

        # retrieve data based on extracted data parameters from the llm
        llm_response['output']['data_to_plot'] = (
            extract_data_from_llm_response(llm_response['output']['extract_data_params']))

        llm_response['output']['alarm_limits'] = {"rpi_alarms": rpi_alarms,
                                                  "cpi_alarms": cpi_alarms,
                                                  "wpi_alarms": wpi_alarms}

        return Response(llm_response)
