"""
Created by PerkinsZhu on 2023/8/17 15:46
"""
from langchain_wenxin import Wenxin
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from com.perkins.base.init import init

init()


class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split("，")


msg = {
    "messages": [
        {"role": "user", "content": "你现在是我的一个助手，我会指定一个类别，你帮我生成该类别下的五个对象，用逗号分隔"},
        {"role": "assistant", "content": "好的，我会严格按照您的要求生成五个对象，并用逗号分隔，其他的都不用输出"},
        {"role": "user", "content": "家具"},
        {"role": "assistant", "content": "沙发，餐桌，椅子，床，书柜"},
        {"role": "user", "content": "{text}"}
    ]
}
template = ChatPromptTemplate.from_messages( [
        {"role": "user", "content": "你现在是我的一个助手，我会指定一个类别，你帮我生成该类别下的五个对象，用逗号分隔"},
        {"role": "assistant", "content": "好的，我会严格按照您的要求生成五个对象，并用逗号分隔，其他的都不用输出"},
        {"role": "user", "content": "家具"},
        {"role": "assistant", "content": "沙发，餐桌，椅子，床，书柜"},
        {"role": "user", "content": "{text}"}
    ])

messages = template.format_messages(
    text="动物"
)

chat_prompt = ChatPromptTemplate.from_messages(messages)


llm = Wenxin(model="ernie-bot-turbo", temperature=0.1)

chain = LLMChain(
    llm=llm,
    prompt=chat_prompt,
    output_parser=CommaSeparatedListOutputParser()
)
print(chain.run("动物"))
