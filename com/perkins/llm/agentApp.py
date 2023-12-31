"""
Created by PerkinsZhu on 2023/8/8 11:22
"""
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

from com.perkins.base.init import init

init();


llm = OpenAI(temperature=0,model_name='gpt-3.5-turbo-16k-0613')
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")
