import urllib

from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from chat.models.chat_model import Chat
from chat.serializers.chat_serializer import ChatSerializer
from chat.services.services.chat_services import ask_openai, extract_data_from_llm_response, set_alarm_limits, \
    get_outside_alarm_limits, extract_trend_info
from reservoir.services.reservoir_measurement_services import calculate_time_vs_pi_trend_lines


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

        if llm_response['plotting'] is not None:
            self.invoke_plot_data_response(llm_response, rpi_alarms, cpi_alarms, wpi_alarms)

        return Response(llm_response)

    @staticmethod
    def invoke_plot_data_response(llm_response, rpi_alarms,
                                  cpi_alarms,
                                  wpi_alarms):
        # retrieve data based on extracted data parameters from the llm
        llm_response['plotting']['data_to_plot'] = (
            extract_data_from_llm_response(llm_response['plotting']['extract_data_params']))

        if llm_response['plotting']['data_to_plot'] is None:
            llm_response['plotting'] = None
            llm_response['chat_response'] = "Could not find any data for this well."
            return Response(llm_response)

        llm_response['plotting']['alarm_limits'] = set_alarm_limits(rpi_alarms, cpi_alarms, wpi_alarms)

        # alarms
        llm_response['plotting']['alarm_response'] = get_outside_alarm_limits(llm_response['plotting']['data_to_plot'],
                                                             llm_response['plotting']['alarm_limits'])

        # trends
        llm_response['plotting']['data_to_plot'] = calculate_time_vs_pi_trend_lines(llm_response['plotting']['data_to_plot'])
        llm_response['plotting']['trend_response'] = extract_trend_info(llm_response['plotting']['data_to_plot'])

        return Response(llm_response)
