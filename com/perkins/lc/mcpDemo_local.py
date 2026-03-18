from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务（官方标准写法）
mcp = FastMCP("demo-skill")

# 定义 MCP 工具
@mcp.tool()
def hello(name: str) -> str:
    """向用户打招呼"""
    return f"你好 {name}！这是标准 MCP 协议工具"

@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个数之和"""
    return a + b

# 启动
if __name__ == "__main__":
    print("✅ MCP 标准 Skill 已启动")
    mcp.run()