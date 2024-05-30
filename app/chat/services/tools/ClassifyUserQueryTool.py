from langchain_community.chat_models import ChatOpenAI
from langchain_core.tools import BaseTool


class ClassifyUserQueryTool(BaseTool):
    name = "ClassifyUserQueryTool"
    description = "Always run this tool first. Classify the user query into one of three different categories."

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt = f""" Based on the user query, try to classify the question into one of three different categories.
        The categories are: Graph plotting, knowledge search and monitor alarms. If you cannot classify into 
        any of these categories, inform the user and ask for a more specific question.
        
        Use these example questions to calibrate categories:
        
            Knowledge search:
                -What are performance indicators?
                -What is cpi?
                -What does it mean when wpi drops?
                -How can i prevent a drop of wpi?
                
            Monitor alarms:
                -What is the safe pressure range to maintain cpi above 0.8? 
                -When will wpi exceed the alarm threshold? 
                -When does cpi exceed alarm?
                -When does wpi exceed the threshold?

          ,\nQuestion: {user_query}\n
    """
        classification = llm.invoke(prompt)

        return classification

