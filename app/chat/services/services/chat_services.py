import json
import urllib

import numpy as np

from chat.services.agent.get_agent_executor import get_agent_executor


def ask_openai(user_prompt):
    if isinstance(user_prompt, list):
        user_prompt = json.dumps(user_prompt)
    parsed_user_prompt = urllib.parse.unquote(user_prompt)

    agent = get_agent_executor()
    response = agent.invoke({"input": parsed_user_prompt})

    try:
        return json.loads(response['output'])
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def extract_data_from_llm_response(well_name, data_params):
    if data_params is None:
        return None

    x_axis_dimension = data_params.get('x_axis_dimension')
    y_axis_dimensions = data_params.get('y_axis_dimensions')

    with open('reservoir/data/static_reservoir_data.json', 'r') as f:
        static_reservoir_data = json.load(f)

    # find correct well data
    well_data = [item for item in static_reservoir_data
                     if item['well_name'] == well_name]

    # could not find any data for this well
    if len(well_data) == 0:
        return None

    # filter based on llm response parameters
    required_attributes = [well_name, x_axis_dimension] + y_axis_dimensions

    filtered_data = [{k: item[k] for k in required_attributes if k in item}
                     for item in well_data]

    return filtered_data


def set_alarm_limits(rpi_alarms, cpi_alarms, wpi_alarms):
    return {"rpi": rpi_alarms, "cpi": cpi_alarms, "wpi": wpi_alarms}


def get_outside_alarm_limits(data_to_plot, alarm_limits):
    alarm_info = []
    for datapoint in data_to_plot:
        for alarm_type, alarm_value in alarm_limits.items():
            lower_limit, upper_limit = alarm_value
            if alarm_type in datapoint and (datapoint[alarm_type] < lower_limit or datapoint[alarm_type] > upper_limit):
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
                alarm_info.append(f"The alarm for {alarm_type} is {datapoint_outside_limit['status']} at "
                                  f"{datapoint_outside_limit['start_time']}.")

    return alarm_info


def extract_trend_info(json_data):
    different_trend_datapoints = [2, 4, 13, 18]
    trend_info = []

    for trend_number, i in enumerate(different_trend_datapoints, start=1):
        if 'cpi' in json_data[i]:
            cpi_slope = json_data[i][f'cpi_slope_{trend_number}']
            cpi_intercept = json_data[i][f'cpi_intercept_{trend_number}']
            cpi_trend = 'increasing' if cpi_slope > 0 else 'decreasing'
            trend_info.append(f"Trend {trend_number} for CPI is {cpi_trend} with equation y = {round(cpi_slope, 6)}*x + {round(cpi_intercept, 6)}.")

        if 'rpi' in json_data[i]:
            rpi_slope = json_data[i][f'rpi_slope_{trend_number}']
            rpi_intercept = json_data[i][f'rpi_intercept_{trend_number}']
            rpi_trend = 'increasing' if rpi_slope > 0 else 'decreasing'
            trend_info.append(f"Trend {trend_number} for RPI is {rpi_trend} with equation y = {round(rpi_slope, 6)}*x + {round(rpi_intercept, 6)}.")

        if 'wpi' in json_data[i]:
            wpi_slope = json_data[i][f'wpi_slope_{trend_number}']
            wpi_intercept = json_data[i][f'wpi_intercept_{trend_number}']
            wpi_trend = 'increasing' if wpi_slope > 0 else 'decreasing'
            trend_info.append(f"Trend {trend_number} for WPI is {wpi_trend} with equation y = {round(wpi_slope, 6)}*x + {round(wpi_intercept, 6)}.")

    return trend_info


def calculate_trend_response(performance_indicator, trend_number, rpi_alarms, cpi_alarms, wpi_alarms, well_name):
    # retrieve data
    with open('reservoir/data/static_reservoir_data.json', 'r') as f:
        static_reservoir_data = json.load(f)

    # find correct well data
    well_data = [item for item in static_reservoir_data if item['well_name'] == well_name]

    if trend_number == 1:
        well_data = well_data[0:3]
    elif trend_number == 2:
        well_data = well_data[2:12]
    elif trend_number == 3:
        well_data = well_data[11:17]
    elif trend_number == 4:
        well_data = well_data[16:23]

    times = [data['start_time'] for data in well_data]
    alarms = rpi_alarms if performance_indicator == 'rpi' else cpi_alarms if performance_indicator == 'cpi' \
        else wpi_alarms

    values = [data[performance_indicator] for data in well_data]
    (slope, intercept), residuals, _, _, _ = np.polyfit(times, values, 1, full=True)

    upper_alarm_time = (alarms[1] - intercept) / slope if slope != 0 else None
    lower_alarm_time = (alarms[0] - intercept) / slope if slope != 0 else None

    response = (f"""
    The trend line for {performance_indicator} is y = {round(slope, 6)}*time(hours) + {round(intercept, 6)} at 
    phase {trend_number}. For lower ({alarms[0]}) and upper ({alarms[1]}) alarms it will
    exceed the alarm threshold at time {round(lower_alarm_time)} and {round(upper_alarm_time)}.
                """)

    return response
