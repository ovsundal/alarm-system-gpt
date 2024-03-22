import json
import urllib

from chat.services.agent.get_agent_executor import get_agent_executor


def ask_openai(user_prompt):
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
