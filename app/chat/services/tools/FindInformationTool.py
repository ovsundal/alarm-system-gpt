import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import BaseTool
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader


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
        self._setup_and_feed_database()

        return "Knowledge answering is not implemented yet"

    @staticmethod
    def _setup_and_feed_database():
        # load data from pdfs
        print(os.path.abspath(os.getcwd()))
        loaders = [
            PyPDFLoader("chat/services/background-knowledge/PTA_metrics_for_time_lapse_analysis_of_well_performance.pdf")
            # PyPDFLoader("./background_knowledge/data/well_performance_metrics_suitable_for_automated_well_monitoring.pdf")
        ]

        docs = []
        for loader in loaders:
            docs.extend(loader.load())

        # split data
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=150
        )

        splits = text_splitter.split_documents(docs)


        print("splits length")
        print(len(splits))

        # embedding
        embedding = OpenAIEmbeddings()
        persist_directory = './chroma/'

        # remove old database files if any
        command = "rm -rf ./docs/chroma"
        os.system(command)

        # create db
        vectordb = Chroma.from_documents(
            documents=splits,
            embedding=embedding,
            persist_directory=persist_directory
        )

        vectordb.persist()

        print("vectordb._collection.count()")
        print(vectordb._collection.count())

        pass
