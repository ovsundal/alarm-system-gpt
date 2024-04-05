from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def get_chat_prompt():
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant, specialized in oilfield reservoirs. \
             For all queries, always run the custom tool 'ClassifyUserQueryTool' \
             and return result from that tool to the user. Return everything as a json object not a string. \
             The json object should have the following format: \
             {{\
             extract_data_params: add extracted parameters from AnswerHistoryQuestionsTool here. "
                       "If this tool was not used in the query, use None as value, \
             original_query: the original user query, \
             chat_response: "
                       "If you ran the ExtractParametersForPlottingTool: "
                           "if you were able to extract data params, inform the user that the graph has been plot."
                           "Mention what parameters were plot, and that the graph can be seen in the LLM response pane \
                        If you ran the FindInformationTool: \
                            If you were able to find information, return the information to the user. \
                            If you were not able to find information, inform the user that the information could not be "
                            "found. \
             }}\
             "),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
