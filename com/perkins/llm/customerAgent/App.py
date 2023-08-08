"""
Created by PerkinsZhu on 2023/8/8 13:40
"""
from com.perkins.llm.customerAgent.FakeAgent import FakeAgent
from langchain.agents import Tool, AgentExecutor, BaseSingleActionAgent
from langchain import OpenAI, SerpAPIWrapper
from com.perkins.base.init import init
init()


search = SerpAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
        return_direct=True
    )
]


agent = FakeAgent()
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
agent_executor.run("2023年上海有多少人？")