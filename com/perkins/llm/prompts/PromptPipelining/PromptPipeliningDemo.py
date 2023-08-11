"""
Created by PerkinsZhu on 2023/8/11 13:40
"""

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from com.perkins.base.init import init
init()

prompt = (
    PromptTemplate.from_template("Tell me a joke about {topic}")
    + ", make it funny"
    + "\n\nand in {language}"
)

res = prompt.format(topic="sports", language="spanish")
print(res)

model = ChatOpenAI()
chain = LLMChain(llm=model, prompt=prompt)
res = chain.run(topic="sports", language="spanish")
print(res)
