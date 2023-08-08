"""
Created by PerkinsZhu on 2023/8/8 9:17
"""
import os

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from com.perkins.base.init import init

from langchain.llms import openai

init()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 读取档案
file_path = "./test.txt"
loader = file_path.endswith(".pdf") and PyPDFLoader(file_path) or TextLoader(file_path)

# 选择 splitter 并将文字切分成多个 chunk
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = loader.load_and_split(splitter)

# 建立本地 db
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# 对话 chain
qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0), vectorstore.as_retriever())
chat_history = []
while True:
    query = input('\nQ: ')
    if not query:
        break
    result = qa({"question": query + ' (中文回答)', "chat_history": chat_history})
    print('A:', result['answer'])
    chat_history.append((query, result['answer']))
