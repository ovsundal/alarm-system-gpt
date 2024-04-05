from langchain.tools import BaseTool
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class FindInformationTool(BaseTool):
    name = "FindInformationTool"
    description = """Searches a vector database for information that answers the user query. 
    Always run this tool if the user query is classified as a knowledge search.
    """

    def _run(self, user_query):
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Search the database and find information that answer the user query."),
            ("human", "{user_query}")
        ])

        return "Knowledge answering is not implemented yet"
