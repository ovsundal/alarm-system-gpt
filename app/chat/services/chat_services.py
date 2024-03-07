import json

from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

from chat.services.chains.parse_user_prompt import parse_user_prompt

# To control the randomness and creativity of the generated
# text by an LLM, use temperature = 0.0
chat = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.0)

def ask_openai(user_prompt):
    llm_model = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.0)
    memory = ConversationBufferMemory()

    conversation = ConversationChain(
        llm=llm_model,
        memory=memory,
        verbose=True
    )

    parsed_user_prompt = parse_user_prompt(user_prompt)

    with open('chat/services/chains/data_to_llm.json', 'r') as f:
        static_well_data = json.load(f)

    chat_response = conversation.predict(input=parsed_user_prompt)

    return chat_response

