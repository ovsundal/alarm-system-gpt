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
        data['temperature'] = round(data['temperature'], 2)
        data['wpi'] = round(data['wpi'], 2)
        data['rpi'] = round(data['rpi'], 2)
        data['cpi'] = round(data['cpi'], 2)

    return well_data


def calculate_trend_lines(well_data):

    # Split the well_data
    trend1_data = well_data[0:4]
    trend2_data = well_data[3:12]
    trend3_data = well_data[11:17]
    trend4_data = well_data[16:23]

    trend1_data = calculate_and_add_slope_intercept_and_r_squared(trend1_data, 1)
    trend2_data = calculate_and_add_slope_intercept_and_r_squared(trend2_data, 2)
    trend3_data = calculate_and_add_slope_intercept_and_r_squared(trend3_data, 3)
    trend4_data = calculate_and_add_slope_intercept_and_r_squared(trend4_data, 4)

    return trend1_data[:-1] + trend2_data[:-1] + trend3_data[:-1] + trend4_data


def calculate_and_add_slope_intercept_and_r_squared(trend_line_data, trend_number):
    # Extract the start_time, wpi, and rpi values for trend_line_data
    times = [data['start_time'] for data in trend_line_data]
    wpi_values = [data['wpi'] for data in trend_line_data]
    rpi_values = [data['rpi'] for data in trend_line_data]
    cpi_values = [data['cpi'] for data in trend_line_data]

    # Calculate the wpi and rpi slopes, intercepts, and R^2
    (wpi_slope, wpi_intercept), residuals, _, _, _ = np.polyfit(times, wpi_values, 1, full=True)
    wpi_r_squared = 1 - residuals / (len(wpi_values) * np.var(wpi_values))

    (rpi_slope, rpi_intercept), residuals, _, _, _ = np.polyfit(times, rpi_values, 1, full=True)
    rpi_r_squared = 1 - residuals / (len(rpi_values) * np.var(rpi_values))

    (cpi_slope, cpi_intercept), residuals, _, _, _ = np.polyfit(times, cpi_values, 1, full=True)
    cpi_r_squared = 1 - residuals / (len(cpi_values) * np.var(cpi_values))

    # Add the slopes, intercepts, and R^2 to each dictionary in the trend_line_data list
    for data in trend_line_data:
        data[f'wpi_slope_{trend_number}'] = wpi_slope
        data[f'wpi_intercept_{trend_number}'] = wpi_intercept
        data[f'wpi_r_squared_{trend_number}'] = np.round(wpi_r_squared, 3)
        data[f'rpi_slope_{trend_number}'] = rpi_slope
        data[f'rpi_intercept_{trend_number}'] = rpi_intercept
        data[f'rpi_r_squared_{trend_number}'] = np.round(rpi_r_squared, 3)
        data[f'cpi_slope_{trend_number}'] = cpi_slope
        data[f'cpi_intercept_{trend_number}'] = cpi_intercept
        data[f'cpi_r_squared_{trend_number}'] = np.round(cpi_r_squared, 3)

    return trend_line_data


def extend_timelines(well_data):
    # Extend the trend lines 10000 hours (~1 year) to the future
    future_time = well_data[-1]['start_time'] + 10000

    well_data.append({
        'start_time': future_time,
        'wpi_slope_4': well_data[-1]['wpi_slope_4'],
        'wpi_intercept_4': well_data[-1]['wpi_intercept_4'],
        'wpi_r_squared_4': well_data[-1]['wpi_r_squared_4'],
        'rpi_slope_4': well_data[-1]['rpi_slope_4'],
        'rpi_intercept_4': well_data[-1]['rpi_intercept_4'],
        'rpi_r_squared_4': well_data[-1]['rpi_r_squared_4'],
        'cpi_slope_4': well_data[-1]['cpi_slope_4'],
        'cpi_intercept_4': well_data[-1]['cpi_intercept_4'],
        'cpi_r_squared_4': well_data[-1]['cpi_r_squared_4'],
    })

    return well_data
