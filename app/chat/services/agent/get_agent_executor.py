from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.chat_models import ChatOpenAI
from langsmith.run_helpers import traceable

from chat.services.agent.chat_prompt_template import get_chat_prompt
from chat.services.tools.ExtractParametersForEvaluatingTrendTool import ExtractParametersForEvaluatingTrendTool
from chat.services.tools.ExtractParametersForPlottingTool import ExtractParametersForPlottingTool
from chat.services.tools.ClassifyUserQueryTool import ClassifyUserQueryTool
from chat.services.tools.FindInformationTool import FindInformationTool


@traceable
def get_agent_executor():
    llm_model = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.0)
    tools = [ClassifyUserQueryTool(), ExtractParametersForPlottingTool(), FindInformationTool(), ExtractParametersForEvaluatingTrendTool()]
    agent = create_openai_functions_agent(llm_model, tools, get_chat_prompt())

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        callbacks=[])
