import unittest
# 导入LangChain并验证版本
import langchain

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


    def test_langchain_env(self):
        print(langchain.__version__)  # 输出版本号（如0.2.0）
        # 测试Ollama集成（需提前启动Ollama）
        from langchain_ollama import OllamaLLM
        llm = OllamaLLM(model="deepseek-r1")
        print(llm.invoke("你好，测试一下"))  # 输出模型回答则成功






if __name__ == '__main__':
    unittest.main()
