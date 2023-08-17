"""
Created by PerkinsZhu on 2023/8/17 16:38
"""
from langchain.prompts import ChatPromptTemplate

from langchain import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate

prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}."
)
print(prompt_template.format(adjective="funny", content="chickens"))

prompt_template = PromptTemplate.from_template("Tell me a joke")
print(prompt_template.format())

invalid_prompt = PromptTemplate(
    input_variables=["adjective", 'content'],
    template="Tell me a {adjective} joke about {content}."
)
print(invalid_prompt.format(adjective="aaa", content="ccc"))

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
])

messages = template.format_messages(
    name="Bob",
    user_input="What is your name?"
)
print(messages)

template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a helpful assistant that re-writes the user's text to "
                "sound more upbeat."
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

print(template.format_messages(text='i dont like eating tasty things.'))
