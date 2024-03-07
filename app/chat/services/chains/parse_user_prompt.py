from langchain_core.prompts import ChatPromptTemplate


def parse_user_prompt(user_prompt):
    # add all answer customization here
    user_style = """
    English in a calm and respectful tone. 
    The user is an oilfield reservoir engineer. 
    Answers should be rather short and concise, 2-3 lines max.
    """

    template_string = """
    Translate the text that is delimited by triple backticks \
    into a style that is {style}. text: ```{text}```
    """

    prompt_template = ChatPromptTemplate.from_template(template_string)

    user_message = prompt_template.format_messages(
        style=user_style,
        text=user_prompt)

    return user_message
