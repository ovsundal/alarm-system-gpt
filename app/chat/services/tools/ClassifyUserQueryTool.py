from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool


class ClassifyUserQueryTool(BaseTool):
    name = "ClassifyUserQuery"
    description = "Always run this tool first. Classify the user query into one of two different categories."

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt = f""" Classify the user question into one of five different categories.
    The input takes the form of a user question. Based on the question, 
    try to classify the question into one of five different categories.
    The categories are: Graph plotting and Summarize alarms outside alarm ranges

        -Graph plotting. 
        If this category is chosen, run the ExtractParametersForPlottingTool.
            Example questions that this tool covers: 
                -Can you plot the performance indicators (PI) over time (or temperature/pressure)?
                -Plot wpi over time for well_x
                -Plot data for well_x

        -Summarize alarms outside alarm ranges.
            If this category is chosen, the next tool in the chain should be SummarizeAlarmsOutsideRangeTool.
            Example input is a json object with the following properties:
                   "'start_time': number, (can be either start_time, pressure, or temperature)"
                   "'status': string, (can be either 'below lower limit' or 'above upper limit')"
                   "'alarm': string, (can be either 'rpi', 'cpi', or 'wpi')"

    ,\nQuestion: {user_query}\n"""
        classification = llm.invoke(prompt)

        return classification
