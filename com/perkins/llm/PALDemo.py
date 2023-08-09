"""
Created by PerkinsZhu on 2023/8/9 17:32
"""

from langchain.chains import PALChain
from langchain import OpenAI
from com.perkins.base.init import init

init()
llm = OpenAI(temperature=0, max_tokens=512)
pal_chain = PALChain.from_math_prompt(llm, verbose=True)
question = "Jan has three times the number of pets as Marcia. Marcia has two more pets than Cindy. If Cindy has four pets, how many total pets do the three have?"
pal_chain.run(question)
