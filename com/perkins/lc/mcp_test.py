from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务
mcp = FastMCP("我的MCP服务",host="192.168.1",port=8777)

# 定义一个工具：问候
@mcp.tool()
def hello(name: str) -> str:
    """向用户发送问候
    :param name: 用户名字
    """
    return f"你好 {name}！我是 MCP 工具返回的内容～"

# 定义一个工具：加法计算
@mcp.tool()
def add(a: int, b: int) -> int:
    """两个数字相加
    :param a: 数字1
    :param b: 数字2
    """
    return a + b

# ========== 启动：Dify 最稳定模式 SSE ==========
if __name__ == "__main__":
    mcp.run(transport="streamable-http")

# dify中地址配置为： http://${ip}:${port}/mcp