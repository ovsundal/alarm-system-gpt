import json

from langchain_community.chat_models import ChatOpenAI


class SummarizeAlarmsOutsideRangeChain:
    def __init__(self, model_name="gpt-4-0125-preview", temperature=0):
        self.model = ChatOpenAI(model=model_name, temperature=temperature)
        self.system_message = """
                Your purpose is to summarize a list of json objects into text. Each object has the following properties:
                 'start_time': number, (can be either start_time, pressure, or temperature)
                 'status': string, (can be either 'below lower limit' or 'above upper limit')
                 'alarm': string, (can be either 'rpi', 'cpi', or 'wpi')

                 Output should be a list where each member is a text summarizing the alarms that are outside of 
                 the alarm range with format: 
                 'The alarm for {alarm_type} is {status} at {start_time}. This list should be sorted by {status}.
                """

    def run(self, json_data):
        json_data_str = json.dumps(json_data)
        full_prompt = f"{self.system_message}\n\nData:\n{json_data_str}"
        response = self.model.invoke(full_prompt)

        return response
