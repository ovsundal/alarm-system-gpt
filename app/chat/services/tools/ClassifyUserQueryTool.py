from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool


class ClassifyUserQueryTool(BaseTool):
    name = "ClassifyUserQuery"
    description = "Always run this tool first. Classify the user query into one of three different categories."

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt = f""" Classify the user question into one of five different categories.
        The input takes the form of a user question. Based on the question, 
        try to classify the question into one of two different categories.
        The categories are: Graph plotting, knowledge search and evaluate trends.

          ,\nQuestion: {user_query}\n
    """
        classification = llm.invoke(prompt)

        return classification
