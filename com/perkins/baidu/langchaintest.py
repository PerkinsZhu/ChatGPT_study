"""
Created by PerkinsZhu on 2023/8/16 17:40
"""
from langchain_wenxin import Wenxin
from langchain_wenxin.chat_models import ChatWenxin
from langchain.schema.messages import HumanMessage
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from com.perkins.base.init import init
init()

llm = Wenxin(model="ernie-bot-turbo",temperature=0.1)
# print(llm("今天是什么时候？上海浦东天气怎么样？"))
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Now let's test it out!
print(agent.run("Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?"))

# prompt = PromptTemplate(
#     input_variables=["product"],
#     template="你觉得小米的 {product} 怎么样?",
# )
#
#
# chain = LLMChain(llm=llm, prompt=prompt)
#
#
# print(chain.run("手机"))



