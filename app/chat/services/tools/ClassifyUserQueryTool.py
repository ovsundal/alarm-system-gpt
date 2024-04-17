from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool


class ClassifyUserQueryTool(BaseTool):
    name = "ClassifyUserQuery"
    description = "Always run this tool first. Classify the user query into one of three different categories."

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt = f""" Based on the user query, try to classify the question into one of three different categories.
        The categories are: Graph plotting, knowledge search and evaluate trends. If you cannot classify into 
        any of these categories, inform the user and ask for a more specific question.

          ,\nQuestion: {user_query}\n
    """
        classification = llm.invoke(prompt)

        return classification

