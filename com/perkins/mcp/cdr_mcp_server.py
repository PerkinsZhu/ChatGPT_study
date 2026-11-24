from mcp.server.mcpserver import MCPServer

mcp = MCPServer("cdr-query-server")

@mcp.tool()
def query_cdr(call_id: str | None = None, caller: str | None = None, callee: str | None = None, time_start: str | None = None, time_end: str | None = None):
    """
    查询通话 CDR 记录
    :param call_id: 呼叫唯一ID
    :param caller: 主叫号码
    :param callee: 被叫号码
    :param time_start: 起始时间，格式 2026-11-24 10:00:00
    :param time_end: 结束时间
    """
    if call_id == "abc123":
        return {
            "call_id": "abc123",
            "sip_code": "486",
            "hangup_cause": "USER_BUSY",
            "start_time": "2026-11-24 10:05:00",
            "end_time": "2026-11-24 10:05:03"
        }
    return {"msg": "没有找到对应的通话记录"}

if __name__ == "__main__":
    mcp.run()
