from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import create_structured_output_runnable


class ExtractParametersForEvaluatingTrendToolStructuredOutputFormat(BaseModel):
    performance_indicator: str = Field(default="cpi", description="""The performance indicator to be evaluated.
    Possible values are cpi, rpi or wpi.""")
    trend_number: int = Field(default=4, description="""The number of the trend line to be evaluated. 
    Possible values are 1, 2, 3 or 4, where 4 is default if not specified.""")

    class Config:
        schema_extra = {
            "example": {
                "performance_indicator": "cpi",
                "trend_number": 4
            }
        }


class ExtractParametersMonitorAlarmTool(BaseTool):
    name = "ExtractParametersMonitorAlarmTool"
    description = """
     Use this tool whenever the user asks about when a performance indicator (cpi, wpi or rpi) exceeds an alarm limit. 
    Run this tool whenever the user query is evaluated to be in the 'evaluate trends' category.
    Example questions are: 
        -When will wpi exceed the alarm treshold? 
        -When does cpi exceed alarm?
        -When does wpi exceed alarm in phase 2?
        
    Extracts parameters from the user query, formatted exactly as defined in 
    ExtractParametersForEvaluatingTrendToolStructuredOutputFormat. Always define the output like this:
     'trends': {
        performance_indicator: str,
        trend_number: int
     }
     
     These parameters should be returned to the user,
     and will be used to extract well data outside of the LLM universe. Always run this tool if the user query is 
     classified as am evaluate trends query.
    """

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Extract the performance_indicator and trend_number from the users query."""),
            ("human", "{user_query}")
        ])

        runnable = create_structured_output_runnable(ExtractParametersForEvaluatingTrendToolStructuredOutputFormat, llm,
                                                     prompt_template)
        return runnable.invoke({"user_query": user_query}).dict()