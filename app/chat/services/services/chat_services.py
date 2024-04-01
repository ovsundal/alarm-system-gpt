import json
import urllib

from chat.services.agent.get_agent_executor import get_agent_executor


def ask_openai(user_prompt):
    if isinstance(user_prompt, list):
        user_prompt = json.dumps(user_prompt)
    parsed_user_prompt = urllib.parse.unquote(user_prompt)

    agent = get_agent_executor()
    response = agent.invoke({"input": parsed_user_prompt})
    response['output'] = json.loads(response['output'])

    return response


def extract_data_from_llm_response(data_params):
    if data_params is None:
        return None

    well_name = data_params.get('well_name')
    x_axis_dimension = data_params.get('x_axis_dimension')
    y_axis_dimensions = data_params.get('y_axis_dimensions')

    with open('reservoir/data/static_reservoir_data.json', 'r') as f:
        static_reservoir_data = json.load(f)

    # find correct well data
    well_data = [item for item in static_reservoir_data
                     if item['well_name'] == well_name]

    # filter based on llm response parameters
    required_attributes = [well_name, x_axis_dimension] + y_axis_dimensions

    filtered_data = [{k: item[k] for k in required_attributes if k in item}
                     for item in well_data]

    return filtered_data


def set_alarm_limits(rpi_alarms, cpi_alarms, wpi_alarms):
    return {"rpi": rpi_alarms, "cpi": cpi_alarms, "wpi": wpi_alarms}


def get_outside_alarm_limits(data_to_plot, alarm_limits):
    datapoints_outside_limits = []

    for datapoint in data_to_plot:
        for alarm_type, alarm_value in alarm_limits.items():
            lower_limit, upper_limit = alarm_value
            if datapoint[alarm_type] < lower_limit or datapoint[alarm_type] > upper_limit:
                datapoint_outside_limit = {
                    'alarm': alarm_type,
                    'status': 'below lower limit' if datapoint[alarm_type] < lower_limit
                    else 'above upper limit'
                }
                if 'start_time' in datapoint:
                    datapoint_outside_limit['start_time'] = round(datapoint['start_time'])
                if 'pressure' in datapoint:
                    datapoint_outside_limit['pressure'] = round(datapoint['pressure'])
                if 'temperature' in datapoint:
                    datapoint_outside_limit['temperature'] = round(datapoint['temperature'])
                datapoints_outside_limits.append(datapoint_outside_limit)

    return datapoints_outside_limits
