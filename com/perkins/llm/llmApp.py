"""
Created by PerkinsZhu on 2023/8/7 9:22
"""
import os

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain import PromptTemplate
from com.perkins.base.init import init

init()
openai_api_key = os.environ["OPENAI_API_KEY"]
openai_api_base = os.environ["OPENAI_API_BASE"]


def simpleTest():
    llm = OpenAI(model_name="gpt-3.5-turbo")
    my_text = "介绍下 ChatGPT "
    print(llm(my_text))


def askTest():
    chat = getChat()
    res = chat(
        [
            # 系统语言
            SystemMessage(content="你是一个智能导游,根据用户描述的地方，回答该地放的特色"),
            # 人类语言
            HumanMessage(content="江苏南京")
        ]
    )
    print(res)


def templeteTest():
    # 使用 openAi 模型
    llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, api_base=openai_api_base)

    # 模版格式
    template = "我想吃{value}。我应该怎么做出来?"
    # 构建模版
    prompt = PromptTemplate(
        input_variables=["value"],
        template=template,
    )
    # 模版生成内容
    final_prompt = prompt.format(value='鱼香肉丝')

    print("输入内容：:", final_prompt)
    print("LLM输出:", llm(final_prompt))


def getChat():
    chat = ChatOpenAI(temperature=1, openai_api_key=openai_api_key, openai_api_base=openai_api_base)
    return chat


def manyMessage():
    chat = getChat()
    batch_messages = [
        [
            SystemMessage(content="你现在是个java程序员，现在请按照我的指令写代码"),
            HumanMessage(content="写一个java版的冒泡排序")
        ],
        [
            SystemMessage(content="你现在是一个数学老师，请帮我计算给你的公式"),
            HumanMessage(content="计算公式： (100*20+200)/9")
        ],
    ]
    result = chat.generate(batch_messages)
    print(result)


if __name__ == '__main__':
    # manyMessage()
    templeteTest()
