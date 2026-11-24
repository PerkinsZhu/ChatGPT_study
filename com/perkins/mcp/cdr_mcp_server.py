from mcp.server.mcpserver import MCPServer

mcp = MCPServer("cdr-query-server")

@mcp.tool()
def query_cdr(call_id: str | None = None, caller: str | None = None, callee: str | None = None, time_start: str | None = None, time_end: str | None = None):
    """查询通话 CDR 记录"""
    if call_id == "abc123":
        return {
            "call_id": "abc123",
            "sip_code": "486",
            "hangup_cause": "USER_BUSY",
            "start_time": "2026-11-24 10:05:00",
            "end_time": "2026-11-24 10:05:03"
        }
    elif call_id == "abc456":
        return {
            "call_id": "abc456",
            "sip_code": "487",
            "hangup_cause": "REQUEST_TIMEOUT",
            "start_time": "2026-11-24 10:06:00",
            "end_time": "2026-11-24 10:06:30"
        }
    elif call_id == "abc789":
        return {
            "call_id": "abc789",
            "sip_code": "503",
            "hangup_cause": "SERVICE_UNAVAILABLE",
            "start_time": "2026-11-24 10:07:00",
            "end_time": "2026-11-24 10:07:02"
        }
    return {"msg": "没有找到对应的通话记录"}

@mcp.tool()
def query_sip_log(call_id: str):
    """根据 call_id 查询详细 SIP 信令日志"""
    return {
        "call_id": call_id,
        "log": "INVITE 发送后无远端 180/200 响应，媒体协商失败，大概率网络/防火墙拦截"
    }

@mcp.tool()
def query_prometheus(metric: str, time_start: str, time_end: str):
    """查询呼叫平台监控指标"""
    return {
        "metric": metric,
        "concurrent_call": 1240,
        "error_rate": "12.3%",
        "tip": "当前线路并发高，服务过载"
    }

if __name__ == "__main__":
    mcp.run()
