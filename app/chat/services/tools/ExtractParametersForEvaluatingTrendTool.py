from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.openai_functions import create_structured_output_runnable


class ExtractParametersForEvaluatingTrendToolStructuredOutputFormat(BaseModel):
    performance_indicator: str = Field(description="""
    Possible values are wpi (well), rpi (reservoir) or cpi (connection) productivity index
    """)

    class Config:
        schema_extra = {
            "example": {
                "performance_indicator": "cpi"
            }
        }


class ExtractParametersForEvaluatingTrendTool(BaseTool):
    name = "ExtractParametersForEvaluatingTrendTool"
    description = """
     Use this tool whenever the user asks a question about specific data. 
    Run this tool whenever the user query is evaluated to be in the evaluate information category.
    Example questions are: 
        -When will wpi exceed the alarm treshold? 
        
    Extracts parameters from the user query. These parameters should be returned to the user,
     and will be used to extract well data outside of the LLM universe. Always run this tool if the user query is 
     classified as am evaluate trends query.
    """

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Extract the performance indicator from the user's query."),
            ("human", "{user_query}")
        ])

        runnable = create_structured_output_runnable(ExtractParametersForEvaluatingTrendToolStructuredOutputFormat, llm,
                                                     prompt_template)
        return runnable.invoke({"user_query": user_query}).dict()
