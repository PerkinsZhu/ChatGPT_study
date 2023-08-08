"""
Created by PerkinsZhu on 2023/8/7 9:39
"""
from langchain import PromptTemplate
from langchain.llms import OpenAI

from com.perkins.base.init import init

init()
# 使用 openAi 模型
llm = OpenAI(model_name="gpt-3.5-turbo")

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
