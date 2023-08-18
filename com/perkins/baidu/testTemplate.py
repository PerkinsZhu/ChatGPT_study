"""
Created by PerkinsZhu on 2023/8/17 16:38
"""
from langchain.prompts import ChatPromptTemplate

from langchain import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
import inspect
from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel, validator


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



# +++++++++++++++++++++++ 自定义模板 ====================================

def get_source_code(function_name):
    # Get the source code of the function
    return inspect.getsource(function_name)


PROMPT = """\
Given the function name and source code, generate an English language explanation of the function.
Function Name: {function_name}
Source Code:
{source_code}
Explanation:
"""


class FunctionExplainerPromptTemplate(StringPromptTemplate, BaseModel):
    """A custom prompt template that takes in the function name as input, and formats the prompt template to provide the source code of the function."""

    @validator("input_variables")
    def validate_input_variables(cls, v):
        """Validate that the input variables are correct."""
        if len(v) != 1 or "function_name" not in v:
            raise ValueError("function_name must be the only input_variable.")
        return v

    def format(self, **kwargs) -> str:
        # Get the source code of the function
        source_code = get_source_code(kwargs["function_name"])

        # Generate the prompt to be sent to the language model
        prompt = PROMPT.format(
            function_name=kwargs["function_name"].__name__, source_code=source_code
        )
        return prompt

    def _prompt_type(self):
        return "function-explainer"


fn_explainer = FunctionExplainerPromptTemplate(input_variables=["function_name"])

# Generate a prompt for the function "get_source_code"
prompt = fn_explainer.format(function_name=get_source_code)
print(prompt)