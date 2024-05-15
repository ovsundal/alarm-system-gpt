from langchain.chains.openai_functions import create_structured_output_runnable
from langchain.tools import BaseTool
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field


class ExtractParametersForPlottingStructuredOutputFormat(BaseModel):
    x_axis_dimension: str = Field(default="start_time", description="""X-axis dimension, possible values are start_time and 
                                                                    pressure. start_time is default if 
                                                                    not specified""")

    y_axis_dimensions: list[str] = Field(default=["wpi", "rpi", "cpi"],
                                         description="""Y-axis dimensions, possible values "
                                                     "are wpi (well), rpi (reservoir) and cpi (connection) productivity 
                                                     indicator, any combination of those three are valid. If the user 
                                                     does not specify what kind of data, then set all three. 
                                                     If X-axis dimension is pressure, then only set rpi.""")

    graph_description: str = Field(default="A graph showing the performance of the well over time.",
                                   description="""A description of the graph that will be generated. Mention what
                                               parameters the graph is showing, on both x and y axis. """)

    class Config:
        schema_extra = {
            "example": {
                "x_axis_dimension": "start_time",
                "y_axis_dimensions": ["wpi", "rpi", "cpi"],
                "graph_description": "Graph showing the performance of the well over time."
            }
        }


class ExtractParametersForPlottingTool(BaseTool):
    name = "ExtractParametersForPlottingTool"
    description = """Extracts parameters from the user query. These parameters should be returned to the user,
     and will be used to extract well data outside of the LLM universe. Always run this tool if the user query is 
     classified as a plotting query.
    """

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Extract the x-axis dimension, and y-axis dimensions from the user's query."),
            ("human", "{user_query}")
        ])

        runnable = create_structured_output_runnable(ExtractParametersForPlottingStructuredOutputFormat, llm,
                                                     prompt_template)
        return runnable.invoke({"user_query": user_query}).dict()

