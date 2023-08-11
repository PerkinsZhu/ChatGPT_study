"""
Created by PerkinsZhu on 2023/8/11 13:24
"""
# All prompts are loaded through the `load_prompt` function.
from langchain.prompts import load_prompt

prompt = load_prompt("simple_prompt.yaml")
print(prompt.format(adjective="funny", content="chickens"))


prompt = load_prompt("simple_prompt.json")
print(prompt.format(adjective="funny", content="chickens"))


prompt = load_prompt("simple_prompt_with_template_file.json")
print(prompt.format(adjective="funny", content="chickens"))


prompt = load_prompt("few_shot_prompt.yaml")
print(prompt.format(adjective="funny"))



