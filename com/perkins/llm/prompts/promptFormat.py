"""
Created by PerkinsZhu on 2023/8/11 9:39
"""
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema import HumanMessage, AIMessage

jinja2_template = "Tell me a {{ adjective }} joke about {{ content }}"
prompt = PromptTemplate.from_template(jinja2_template, template_format="jinja2")

res = prompt.format(adjective="funny", content="chickens")
# Output: Tell me a funny joke about chickens.

print(res)



fstring_template = """Tell me a {adjective} joke about {content}"""
prompt = PromptTemplate.from_template(fstring_template)

res = prompt.format(adjective="funny", content="chickens")
# Output: Tell me a funny joke about chickens.
print(res)



human_prompt = "Summarize our conversation so far in {word_count} words."
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)

chat_prompt = ChatPromptTemplate.from_messages([MessagesPlaceholder(variable_name="conversation"), human_message_template])


human_message = HumanMessage(content="What is the best way to learn programming?")
ai_message = AIMessage(content="""\
1. Choose a programming language: Decide on a programming language that you want to learn.

2. Start with the basics: Familiarize yourself with the basic programming concepts such as variables, data types and control structures.

3. Practice, practice, practice: The best way to learn programming is through hands-on experience\
""")

res = chat_prompt.format_prompt(conversation=[human_message, ai_message], word_count="10")
print(res)