from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import create_structured_output_runnable


class ExtractParametersForEvaluatingTrendToolStructuredOutputFormat(BaseModel):
    """
    The structured output format for the ExtractParametersForEvaluatingTrendTool.
    """
    performance_indicator: str = Field(default="cpi", description="""The performance indicator to be evaluated.
    Possible values are cpi (connection), rpi (reservoir) or wpi (well) performance indicators.""")

    threshold_value: float = Field(default=None, description="""The threshold value to be evaluated.     
    """)

    level_indicator: str = Field(default=None, description="""The level indicator to be evaluated. Possible values are either 
    'above' or 'below'. Set as None if not specified.""")

    action: str = Field(default="trend", description="""The action to be done, based on available query parameters.
    Possible values are trend and pressure_range. If you from the query could not find both threshold_value and 
    level_indicator, then this is trend. If you could find both, then this is pressure_range.""")


class ExtractParametersMonitorAlarmTool(BaseTool):
    name = "ExtractParametersMonitorAlarmTool"
    description = """
     Use this tool whenever the user asks about when a performance indicator (cpi, wpi or rpi) exceeds an alarm limit. 
     Run this tool whenever the user query is evaluated to be in the 'evaluate trends' category.
     These parameters should be returned to the user,
     and will be used to extract well data outside of the LLM universe. Always run this tool if the user query is 
     classified as am evaluate trends query.
    """

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Extract the parameters from the users query."""),
            ("human", "{user_query}")
        ])

        runnable = create_structured_output_runnable(
            output_schema=ExtractParametersForEvaluatingTrendToolStructuredOutputFormat, llm=llm,
            prompt=prompt_template)
        return runnable.invoke({"user_query": user_query}).dict()
