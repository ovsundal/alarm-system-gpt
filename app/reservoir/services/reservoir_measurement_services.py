from datetime import datetime


def filter_reservoir_data(well_data):
    """Business logic to process reservoir data"""

    return well_data


def add_time_passed_hr(well_data):
    """Business logic to process reservoir data"""
    earliest_timestamp = datetime.fromisoformat(
        well_data[0]['start_timestamp'])

    # Calculate time_passed_hr for each data point
    for data in well_data:
        current_timestamp = datetime.fromisoformat(
            data['start_timestamp'])
        time_diff = current_timestamp - earliest_timestamp
        time_passed_hr = time_diff.total_seconds() / 3600

        # Add time_passed_hr to the data point
        data['time_passed_hr'] = int(time_passed_hr)

    return well_data


def add_alarm_limits_to_reservoir_data(
        well_data, alarm_lower_limit, alarm_upper_limit):

    for data in well_data:
        data['alarm_lower_limit'] = alarm_lower_limit
        data['alarm_upper_limit'] = alarm_upper_limit

    return well_data
