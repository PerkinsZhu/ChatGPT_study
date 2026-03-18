# 1. 导入核心依赖
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 2. 初始化嵌入模型（用于生成文本向量，本地Ollama）
embeddings = OllamaEmbeddings(model="nomic-embed-text")  # 轻量中文嵌入模型

# 3. 准备测试数据（可替换为本地PDF/文本）
# 方式A：手动创建测试文档
test_docs = [
    Document(
        page_content="企业产品A的核心功能：智能客服、自动化工单、数据分析，定价999元/月",
        metadata={"source": "产品手册", "product": "A"}
    ),
    Document(
        page_content="企业产品B的核心功能：财务报表生成、税务申报，定价1999元/月",
        metadata={"source": "产品手册", "product": "B"}
    ),
    Document(
        page_content="产品A的售后政策：7天无理由退款，全年24小时技术支持",
        metadata={"source": "售后手册", "product": "A"}
    )
]

# 方式B：加载本地PDF（注释掉方式A，取消注释下方代码）
# from langchain_community.document_loaders import PyPDFLoader
# loader = PyPDFLoader("你的文档.pdf")
# test_docs = loader.load()
# # 文本分割（PDF需分割，避免向量维度超限）
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# test_docs = text_splitter.split_documents(test_docs)

# 4. 创建并初始化向量库（存入数据）
# persist_directory：向量库持久化到本地，下次可直接加载
vector_db = Chroma.from_documents(
    documents=test_docs,
    embedding=embeddings,
    persist_directory="./local_chroma_db"  # 本地存储路径
)

# 5. 测试向量库（核心：检索相似内容）
def test_vector_db(query):
    """测试向量库检索效果"""
    # 5.1 相似性检索（返回Top3最相关文档）
    results = vector_db.similarity_search(
        query=query,
        k=3  # 返回前3条结果
    )
    # 5.2 打印检索结果
    print(f"\n=== 检索问题：{query} ===")
    for i, doc in enumerate(results):
        print(f"\n【结果{i+1}】")
        print(f"内容：{doc.page_content}")
        print(f"元数据：{doc.metadata}")
        # 可选：打印相似度分数（需用similarity_search_with_score）
        results_with_score = vector_db.similarity_search_with_score(query, k=3)
        print(f"相似度：{results_with_score[i][1]}")  # 分数越低越相似（Chroma特性）

# 6. 执行测试用例
if __name__ == "__main__":
    # 测试用例1：精准匹配
    test_vector_db("产品A的核心功能和价格")
    # 测试用例2：语义匹配（关键词不同但语义相同）
    test_vector_db("智能客服产品多少钱一个月")
    # 测试用例3：无关查询（验证是否返回低相关结果）
    test_vector_db("公司的考勤制度是什么")