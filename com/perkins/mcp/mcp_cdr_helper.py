import asyncio
import json
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession


async def call_cdr_mcp(call_id: str | None = None, caller: str | None = None, callee: str | None = None, time_start: str | None = None, time_end: str | None = None):
    params = StdioServerParameters(
        command=r"D:\Anaconda3\envs\agent-dev\python.exe",
        args=[
            r"D:\myproject\pythonProject\ChatGPT_study\com\perkins\mcp\cdr_mcp_server.py"
        ],
    )
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            resp = await session.call_tool(
                "query_cdr",
                arguments={
                    "call_id": call_id,
                    "caller": caller,
                    "callee": callee,
                    "time_start": time_start,
                    "time_end": time_end
                }
            )
            # 解析 TextContent 里面的 json
            text = resp.content[0].text
            return json.loads(text)


if __name__ == "__main__":
    data = asyncio.run(call_cdr_mcp(call_id="abc123"))
    print(data)
