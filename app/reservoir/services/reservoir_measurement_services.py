def filter_reservoir_data(well_data):
    """Business logic to process reservoir data"""

    return well_data


def add_alarm_limits_to_reservoir_data(
        well_data, alarm_lower_limit, alarm_upper_limit):

    for data in well_data:
        data['alarm_lower_limit'] = alarm_lower_limit
        data['alarm_upper_limit'] = alarm_upper_limit

    return well_data
