from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool


class ClassifyUserQueryTool(BaseTool):
    name = "ClassifyUserQuery"
    description = "Always run this tool first. Classify the user query into one of five different categories."

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt = f""" Classify the user question into one of five different categories.

    This should always be the first tool run in the chain. 
    The input takes the form of a user question. Based on the question, 
    try to classify the question into one of five different categories.
    The categories are: Graph plotting, Abnormal behavior detection, 
    trend analysis, abnormal prevention, and background knowledge. These are the only 
    categories you should consider.

        -Graph plotting. 
        If this category is chosen, run the ExtractParametersForPlottingTool.
            Example questions that this tool covers: 
                -Can you plot the performance indicators (PI) over time (or temperature/pressure)?
                -Plot wpi over time for well_x
                -Plot data for well_x

        -Abnormal behavior detection.
            If this category is chosen, the next tool in the chain should be questions_about_abnormal_behavior.
            Example questions:
                -Can you detect any abnormal behavior in well A?

        -Trend analysis. Main output is linear regression analysis.
            If this category is chosen, the next tool in the chain should be questions_about_trend_analysis.
            Example questions:
                -How does RPI change with time? 
                -When will CPI reach 500 psi?

        -Abnormal prevention - Main output are prediction calculations.
            If this category is chosen, the next tool in the chain should be questions_about_abnormal_prevention.
            Example questions:
                -How to prevent the RPI drop below 1.0?

        -Background knowledge. Main output is summarization of the topic based on documentation.
            If this category is chosen, the next tool in the chain should be questions_about_background_knowledge.
            Example questions:
                -What is the definition of RPI?
                -What is the definition of CPI?

    ,\nQuestion: {user_query}\n"""
        classification = llm.invoke(prompt)

        return classification
