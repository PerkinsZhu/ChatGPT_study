import os


def init():
    print("设置环境变量")

    os.environ["OPENAI_API_KEY"] = "sk-kcfJcDXKztSEuMxaSqVjvuniMFIlz8HSr2xApuxivkNINiEc"
    os.environ["OPENAI_API_BASE"] = "https://key.langchain.com.cn/v1"
    os.environ["OPENAI_API_PREFIX"] = "https://key.langchain.com.cn"

    os.environ["OPENAI_API_KEY"] = "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"
    os.environ["OPENAI_API_BASE"] = "http://proxy-chatgpt-jieylpuhdf.us-west-1.fcapp.run/v1"
    # os.environ["OPENAI_API_PREFIX"] = "https://key.langchain.com.cn"


    os.environ["SERPAPI_API_KEY"] = "66a31f5cfa22df3d893c9b7f99a528cb8884ce769735c1ff0482216ca2b5c29b"


    # TODO 已申请key,暂时还未有结果
    os.environ["ANTHROPIC_API_KEY"] = "123"
