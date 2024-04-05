import urllib

from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from chat.models.chat_model import Chat
from chat.serializers.chat_serializer import ChatSerializer
from chat.services.chains.SummarizeAlarmsOutsideRangeChain import SummarizeAlarmsOutsideRangeChain
from chat.services.services.chat_services import ask_openai, extract_data_from_llm_response, set_alarm_limits, \
    get_outside_alarm_limits


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
        print(llm_response)

        if llm_response['output']['extract_data_params'] is not None:
            self.invoke_plot_data_response(llm_response, rpi_alarms, cpi_alarms, wpi_alarms)

        return Response(llm_response)

    @staticmethod
    def invoke_plot_data_response(llm_response, rpi_alarms,
                                  cpi_alarms,
                                  wpi_alarms):
        # retrieve data based on extracted data parameters from the llm
        llm_response['output']['data_to_plot'] = (
            extract_data_from_llm_response(llm_response['output']['extract_data_params']))

        llm_response['output']['alarm_limits'] = set_alarm_limits(rpi_alarms, cpi_alarms, wpi_alarms)

        datapoints_outside_limits = get_outside_alarm_limits(llm_response['output']['data_to_plot'],
                                                             llm_response['output']['alarm_limits'])

        alarm_response = SummarizeAlarmsOutsideRangeChain().run(datapoints_outside_limits)
        llm_response['output']['alarm_response'] = alarm_response.content

        return Response(llm_response)
