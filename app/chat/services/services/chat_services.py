import json

from chat.services.agent.get_agent_executor import get_agent_executor


def ask_openai(user_prompt):

    agent = get_agent_executor()
    response = agent.invoke({"input": "Plot wpi and cpi relative to pressure for well_1"})
    response['output'] = json.loads(response['output'])

    return response


def extract_data_from_llm_response(data_params):
    if data_params is None:
        return None

    print(data_params)
    with open('reservoir/data/static_reservoir_data.json', 'r') as f:
        static_reservoir_data = json.load(f)

    filtered_data = [item for item in static_reservoir_data
                     if item['well_name'] == data_params['well_name']]

    return filtered_data
