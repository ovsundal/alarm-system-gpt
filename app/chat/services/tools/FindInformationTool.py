import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import BaseTool
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAI
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import ContextualCompressionRetriever
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from langchain_community.embeddings.openai import OpenAIEmbeddings


class FindInformationTool(BaseTool):
    name = "FindInformationTool"
    description = """Searches a vector database for information that answers the user query. USe this tool for 
    general questions that can be answered with text. 
    Example questions are:
        -What are performance indicators?
        -What is cpi?
    
    This tool is used
    Always run this tool if the user query is classified as a knowledge search.
    """

    def _run(self, user_query):
        template = """
        Use the following pieces of context to answer the question at the end. If you can't find the answer in context, 
        just say that you don't know, don't try to make up an answer. Use three sentences maximum, and keep the answer 
        as concise as possible. Always include the name of the pdf you got the information from, along with the page
        number at the end of the answer.
        {context}
        Question: {question}
        Helpful Answer:
        """

        if not os.path.exists('chroma/'):
            print('Chroma database not found, creating a new database...')
            vectordb = self._setup_and_feed_database()
        else:
            vectordb = Chroma(persist_directory='./chroma/', embedding_function=OpenAIEmbeddings())

        llm = OpenAI(temperature=0, model="gpt-3.5-turbo-instruct")
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=LLMChainExtractor.from_llm(llm),
            base_retriever=vectordb.as_retriever()
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=compression_retriever,
            return_source_documents=False,
            chain_type_kwargs={"prompt": PromptTemplate.from_template(template)}
        )

        answer = qa_chain({"query": user_query})

        return answer['result']

    @staticmethod
    def _setup_and_feed_database():
        # load data from pdfs
        loaders = [
            PyPDFLoader("chat/services/background-knowledge/PTA_metrics_for_time_lapse_analysis_of_well_performance.pdf"),
            PyPDFLoader("chat/services/background-knowledge/well_performance_metrics_suitable_for_automated_well_monitoring.pdf")
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

        # embedding
        embedding = OpenAIEmbeddings()
        persist_directory = './chroma/'

        # create db
        vectordb = Chroma.from_documents(
            documents=splits,
            embedding=embedding,
            persist_directory=persist_directory
        )

        vectordb.persist()

        return vectordb
