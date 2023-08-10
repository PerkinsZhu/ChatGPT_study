"""
Created by PerkinsZhu on 2023/8/10 13:26
"""

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from com.perkins.base.init import init
from langchain.chains import LLMChain

init()

llm = OpenAI(temperature=0.9)
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}? ",
)

chain = LLMChain(llm=llm, prompt=prompt)

# Run the chain only specifying the input variable.
print(chain.run("colorful socks"))
