import asyncio
import json
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession


async def _mcp_call(tool_name: str, arguments: dict):
    params = StdioServerParameters(
        command=r"D:\Anaconda3\envs\agent-dev\python.exe",
        args=[
            r"D:\myproject\pythonProject\ChatGPT_study\com\perkins\mcp\cdr_mcp_server.py"
        ],
    )
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            resp = await session.call_tool(tool_name, arguments=arguments)
            return json.loads(resp.content[0].text)


async def call_cdr_mcp(call_id: str | None = None, caller: str | None = None, callee: str | None = None):
    return await _mcp_call("query_cdr", {"call_id": call_id, "caller": caller, "callee": callee})


async def call_sip_log_mcp(call_id: str):
    return await _mcp_call("query_sip_log", {"call_id": call_id})


async def call_prom_mcp(metric: str, time_start: str, time_end: str):
    return await _mcp_call("query_prometheus", {"metric": metric, "time_start": time_start, "time_end": time_end})
