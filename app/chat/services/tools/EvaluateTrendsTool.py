from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool


class EvaluateTrendsTool(BaseTool):
    name = "EvaluateTrendsTool"
    description = """
    Use this tool whenever the user asks a question about specific data. 
    Run this tool whenever the user query is evaluated to be in the evaluate information category.
    Example questions are: 
        -When will wpi exceed the alarm treshold? 
    """

    def _run(self, user_query):
        # define the object here
        # llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
    #     prompt = f""" Classify the user question into one of five different categories.
    # The input takes the form of a user question. Based on the question,
    # try to classify the question into one of two different categories.
    # The categories are: Graph plotting and answer questions that requires a knowledge search.
    #
    #     -Graph plotting.
    #     If this category is chosen, run the ExtractParametersForPlottingTool.
    #         Example questions that this tool covers:
    #             -Can you plot the performance indicators (PI) over time (or temperature/pressure)?
    #             -Plot wpi over time for well_x
    #             -Plot data for well_x
    #
    #     -Knowledge search.
    #         If this category is chosen, the next tool in the chain should be FindInformationTool.
    #         Example input is a user question such as:
    #                -What is WPI?
    #                -How do you calculate CPI?
    #
    # ,\nQuestion: {user_query}\n"""
    #     classification = llm.invoke(prompt)

        return "Not implemented"
