"""
Created by PerkinsZhu on 2023/8/9 15:59
"""
from gradio_tools.tools import StableDiffusionTool

from com.perkins.base.init import init
init()

from gradio_tools.tools import StableDiffusionTool

local_file_path = StableDiffusionTool().langchain.run("Please create a photo of a dog riding a skateboard")
local_file_path

print(local_file_path)
# from PIL import Image
#
# im = Image.open(local_file_path)
# display(im)
#
# from langchain.agents import initialize_agent
# from langchain.llms import OpenAI
# from gradio_tools.tools import (StableDiffusionTool, ImageCaptioningTool, StableDiffusionPromptGeneratorTool,
#                                 TextToVideoTool)
#
# from langchain.memory import ConversationBufferMemory
#
# llm = OpenAI(temperature=0)
# memory = ConversationBufferMemory(memory_key="chat_history")
# tools = [StableDiffusionTool().langchain, ImageCaptioningTool().langchain,
#          StableDiffusionPromptGeneratorTool().langchain, TextToVideoTool().langchain]
#
# agent = initialize_agent(tools, llm, memory=memory, agent="conversational-react-description", verbose=True)
# output = agent.run(input=("Please create a photo of a dog riding a skateboard "
#                           "but improve my prompt prior to using an image generator."
#                           "Please caption the generated image and create a video for it using the improved prompt."))
