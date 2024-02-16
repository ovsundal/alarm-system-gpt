import numpy as np


def filter_reservoir_data(well_data):
    """Business logic to process reservoir data"""

    return well_data


def add_alarm_limits_to_reservoir_data(
        well_data, alarm_lower_limit, alarm_upper_limit):

    for data in well_data:
        data['alarm_lower_limit'] = alarm_lower_limit
        data['alarm_upper_limit'] = alarm_upper_limit

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
    # Extract the wpi, rpi, and cpi values along with their corresponding time values
    times = [data['start_time'] for data in well_data]
    wpi_values = [data['wpi'] for data in well_data]
    rpi_values = [data['rpi'] for data in well_data]
    cpi_values = [data['cpi'] for data in well_data]

    # Calculate the best fit lines
    wpi_slope, wpi_intercept = np.polyfit(times, wpi_values, 1)
    rpi_slope, rpi_intercept = np.polyfit(times, rpi_values, 1)
    cpi_slope, cpi_intercept = np.polyfit(times, cpi_values, 1)

    # Apply the trend lines to the data points
    for data in well_data:
        time = data['start_time']
        data['wpi_trend'] = wpi_slope * time + wpi_intercept
        data['rpi_trend'] = rpi_slope * time + rpi_intercept
        data['cpi_trend'] = cpi_slope * time + cpi_intercept

    return well_data

