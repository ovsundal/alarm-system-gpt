import numpy as np


def filter_reservoir_data(well_data):
    """Business logic to process reservoir data"""

    return well_data


def add_alarm_limits_to_reservoir_data(
        well_data, alarms_list):

    [rpi_lower, rpi_upper, cpi_lower, cpi_upper, wpi_lower, wpi_upper] = alarms_list

    for data in well_data:
        data['rpi_alarm_lower_limit'] = rpi_lower
        data['rpi_alarm_upper_limit'] = rpi_upper
        data['cpi_alarm_lower_limit'] = cpi_lower
        data['cpi_alarm_upper_limit'] = cpi_upper
        data['wpi_alarm_lower_limit'] = wpi_lower
        data['wpi_alarm_upper_limit'] = wpi_upper

    return well_data


def round_numbers(well_data):
    for data in well_data:
        data['start_time'] = round(data['start_time'])
        data['pressure'] = round(data['pressure'], 2)
        data['wpi'] = round(data['wpi'], 2)
        data['rpi'] = round(data['rpi'], 2)
        data['cpi'] = round(data['cpi'], 2)

    return well_data


def calculate_time_vs_pi_trend_lines(well_data):
    trend1_data = well_data

    trend1_data = calculate_and_add_slope_intercept_and_r_squared(trend1_data)
    return trend1_data


def calculate_and_add_slope_intercept_and_r_squared(trend_line_data):
    # if start_time is not available, predictions are impossible
    if 'start_time' not in trend_line_data[0]:
        return trend_line_data

    times = [data['start_time'] for data in trend_line_data]

    # when used by the agent, different kind of data may be available, so build in checks to handle data processing
    keys = ['cpi', 'rpi', 'wpi', 'pressure']

    for key in keys:
        if key in trend_line_data[0]:
            values = [data[key] for data in trend_line_data]
            slope, intercept, r_squared = calculate_polyfit_and_r_squared(times, values)

            for data in trend_line_data:
                data[f'{key}_slope_1'] = slope
                data[f'{key}_intercept_1'] = intercept
                data[f'{key}_r_squared_1'] = np.round(r_squared, 3).tolist()

    return trend_line_data


def calculate_polyfit_and_r_squared(x_values, y_values):
    (slope, intercept), residuals, _, _, _ = np.polyfit(x_values, y_values, 1, full=True)
    r_squared = 1 - residuals / (len(y_values) * np.var(y_values))
    return slope, intercept, r_squared

def extend_timelines(well_data):
    # Extend the trend lines 10000 hours (~1 year) to the future
    future_time = well_data[-1]['start_time'] + 10000

    well_data.append({
        'start_time': future_time,
        'cpi_slope_1': well_data[-1]['cpi_slope_1'],
        'cpi_intercept_1': well_data[-1]['cpi_intercept_1'],
        'cpi_r_squared_1': well_data[-1]['cpi_r_squared_1'],
        'cpi_alarm_lower_limit': well_data[-1]['cpi_alarm_lower_limit'],
        'cpi_alarm_upper_limit': well_data[-1]['cpi_alarm_upper_limit'],
        'rpi_slope_1': well_data[-1]['rpi_slope_1'],
        'rpi_intercept_1': well_data[-1]['rpi_intercept_1'],
        'rpi_r_squared_1': well_data[-1]['rpi_r_squared_1'],
        'rpi_alarm_lower_limit': well_data[-1]['rpi_alarm_lower_limit'],
        'rpi_alarm_upper_limit': well_data[-1]['rpi_alarm_upper_limit'],
        'wpi_slope_1': well_data[-1]['wpi_slope_1'],
        'wpi_intercept_1': well_data[-1]['wpi_intercept_1'],
        'wpi_r_squared_1': well_data[-1]['wpi_r_squared_1'],
        'wpi_alarm_lower_limit': well_data[-1]['wpi_alarm_lower_limit'],
        'wpi_alarm_upper_limit': well_data[-1]['wpi_alarm_upper_limit'],
    })

    return well_data
