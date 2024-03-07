from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

# To control the randomness and creativity of the generated
# text by an LLM, use temperature = 0.0
chat = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.0)

# conversation = ConversationChain(
#     llm=chat,
#     memory=memory,
#     verbose=True
# )

template_string = """Translate the text \
that is delimited by triple backticks \
into a style that is {style}. \
text: ```{text}```
"""

prompt_template = ChatPromptTemplate.from_template(template_string)

user_style = """American English \
in a calm and respectful tone
"""


def ask_openai(prompt):
    chat = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.0)
    memory = ConversationBufferMemory()

    conversation = ConversationChain(
        llm=chat,
        memory=memory,
        verbose=True
    )
    user_message = prompt_template.format_messages(
        style=user_style,
        text=prompt)


    parsed_prompt = chat(user_message)
    chat_response = conversation.predict(input=parsed_prompt.content)

    return chat_response

