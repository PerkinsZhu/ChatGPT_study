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


template = """你现在是我的一个助手，我会指定一个类别，你帮我生成该类别下的五个对象，用逗号分隔。注意，不用输出任何提示词，只需要用逗号把五项分隔开即可。"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)


human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

llm = Wenxin(model="ernie-bot-turbo", temperature=0.1)

chain = LLMChain(
    llm=llm,
    prompt=chat_prompt,
    output_parser=CommaSeparatedListOutputParser()
)
print(chain.run("家具"))
