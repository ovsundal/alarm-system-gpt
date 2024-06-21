import urllib

from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from chat.models.chat_model import Chat
from chat.serializers.chat_serializer import ChatSerializer
from chat.services.services.chat_services import ask_openai, extract_data_from_llm_response, set_alarm_limits, \
    get_outside_alarm_limits, extract_trend_info, calculate_trend_response, round_numbers, \
    calculate_pressure_range_response
from reservoir.services.reservoir_measurement_services import calculate_pi_trend_lines


class ChatViewSet(GenericViewSet, CreateModelMixin):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        user_prompt = request.data.get('user_prompt')
        rpi_alarms = request.data.get('rpiAlarmValues')
        cpi_alarms = request.data.get('cpiAlarmValues')
        wpi_alarms = request.data.get('wpiAlarmValues')
        well_name = request.data.get('selectedWellName')
        encoded_user_prompt = urllib.parse.quote(user_prompt)
        llm_response = ask_openai(encoded_user_prompt)

        if llm_response['plotting'] is not None:
            self.invoke_plot_data_response(llm_response, rpi_alarms, cpi_alarms, wpi_alarms, well_name)
        if llm_response['trends'] is not None:
            self.invoke_trend_data_response(llm_response, rpi_alarms, cpi_alarms, wpi_alarms, well_name)

        return Response(llm_response)

    @staticmethod
    def invoke_plot_data_response(llm_response, rpi_alarms,
                                  cpi_alarms,
                                  wpi_alarms, well_name):
        # retrieve data based on extracted data parameters from the llm
        llm_response['plotting']['well_name'] = well_name
        llm_response['plotting']['data_to_plot'] = (
            extract_data_from_llm_response(well_name, llm_response['plotting']['extract_data_params']))

        if llm_response['plotting']['data_to_plot'] is None:
            llm_response['plotting'] = None
            llm_response['chat_response'] = "Could not find any data for this well."
            return Response(llm_response)

        llm_response['plotting']['alarm_limits'] = set_alarm_limits(rpi_alarms, cpi_alarms, wpi_alarms)

        # alarms
        llm_response['plotting']['alarm_response'] = get_outside_alarm_limits(llm_response['plotting']['data_to_plot'],
                                                                              llm_response['plotting']['alarm_limits'])

        # trends
        llm_response['plotting']['data_to_plot'] = calculate_pi_trend_lines(
            llm_response['plotting']['data_to_plot'], llm_response['plotting']['extract_data_params']['x_axis_dimension'])
        llm_response['plotting']['trend_response'] = extract_trend_info(llm_response['plotting']['data_to_plot'])
        llm_response['plotting']['data_to_plot'] = round_numbers(llm_response['plotting']['data_to_plot'])

        return Response(llm_response)

    @staticmethod
    def invoke_trend_data_response(llm_response, rpi_alarms,
                                   cpi_alarms,
                                   wpi_alarms,
                                   well_name):
        if llm_response['trends']['action'] == 'trend':
            llm_response['chat_response'] = calculate_trend_response(llm_response['trends']['performance_indicator'],
                                                                     rpi_alarms,
                                                                     cpi_alarms,
                                                                     wpi_alarms, well_name)
        else:
            llm_response['chat_response'] = calculate_pressure_range_response(llm_response['trends'], well_name)

        return Response(llm_response)
