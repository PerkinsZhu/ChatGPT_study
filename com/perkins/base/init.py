import os


def init():
    print("设置环境变量")
    os.environ["OPENAI_API_KEY"] = "sk-23423434"
    os.environ["OPENAI_API_BASE"] = "https://key.234234.com.cn/v1"
    os.environ["OPENAI_API_PREFIX"] = "https://key.234234.com.cn"
