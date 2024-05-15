from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_chat_prompt():
    return ChatPromptTemplate.from_messages(
        [
            ("system", """
            You are a helpful assistant, specialized in oilfield reservoirs.
             For all queries, always run the custom tool 'ClassifyUserQueryTool'
             and return result from that tool to the user. Return everything as a json object not a string.
             The json object to output must have this exact format (do not use any backticks):
             {{
             original_query: the original user query,
             chat_response: 
                       If you ran the ExtractParametersForPlottingTool: 
                           if you were able to extract data params, inform the user that the graph has been plot.
                           Mention what parameters were plot, and that the graph can be seen in the AI agent response pane 
                        If you ran the FindInformationTool:
                            If you were able to find information, return the information to the user, if not, 
                            inform the user that the information could not be found.
             plotting: This object should be null unless the ExtractParametersForPlottingTool was run. 
                       If so, add the following object:
                            extract_data_params: add extracted parameters from AnswerHistoryQuestionsTool here. 
             }}
             trends: This object should be null unless the ExtractParametersForEvaluatingTrendTool was run. 
                       If so, add the following object:
                            performance_indicator: add extracted parameters from ExtractParametersForEvaluatingTrendTool 
                            here.
             It must be possible to parse this json object using a json.loads() function in Python.
             """),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
