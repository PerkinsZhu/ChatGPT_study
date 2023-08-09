"""
Created by PerkinsZhu on 2023/8/9 17:15
"""

from com.perkins.base.init import init

from langchain import OpenAI, LLMMathChain
init()


llm = OpenAI(temperature=0)
llm_math = LLMMathChain.from_llm(llm, verbose=True)

llm_math.run("半径为5cm的圆的面积是多少？")
