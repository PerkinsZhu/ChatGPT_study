"""
Created by PerkinsZhu on 2023/8/10 14:44
"""

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate

from com.perkins.base.init import init

init()
template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "你现在是一个内容创作者，你将根据我指定的商品写一篇软文在网上推广。生成的内容包括 标题,内容,关键字"
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

llm = ChatOpenAI()
res = llm(template.format_messages(text='小米手机'))
print(res)
