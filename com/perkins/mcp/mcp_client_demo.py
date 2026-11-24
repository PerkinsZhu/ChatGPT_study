import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession


async def main():
    params = StdioServerParameters(
        command=r"D:\Anaconda3\envs\agent-dev\python.exe",
        args=[r"D:\myproject\pythonProject\ChatGPT_study\com\perkins\mcp\cdr_mcp_server.py"],
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("==== 可用工具列表 ====")
            print(tools.tools)

            result = await session.call_tool(
                "query_cdr",
                arguments={"call_id": "abc123"}
            )
            print("\n==== 调用结果 ====")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
