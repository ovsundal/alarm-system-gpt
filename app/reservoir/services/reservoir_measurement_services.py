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
