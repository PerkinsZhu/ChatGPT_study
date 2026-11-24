import asyncio
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from mcp_cdr_helper import call_cdr_mcp, call_sip_log_mcp, call_prom_mcp

import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


class AgentState(TypedDict):
    user_query: str
    call_id: Optional[str]
    caller: Optional[str]
    callee: Optional[str]
    cdr_data: Optional[dict]
    sip_log: Optional[dict]
    prom_data: Optional[dict]
    report: Optional[str]


# ========= 改成你自己的模型配置 =========
llm = ChatOpenAI(
    base_url=os.getenv("base_url", ""),
    api_key=os.getenv("api_key", ""),
    model=os.getenv("model", ""),
)


class ExtractSchema(BaseModel):
    call_id: Optional[str]
    caller: Optional[str]
    callee: Optional[str]


async def extract_param(state: AgentState) -> AgentState:
    resp = await llm.with_structured_output(ExtractSchema).ainvoke(state["user_query"])
    return {
        **state,
        "call_id": resp.call_id,
        "caller": resp.caller,
        "callee": resp.callee
    }


async def fetch_cdr(state: AgentState) -> AgentState:
    cdr = await call_cdr_mcp(
        call_id=state["call_id"],
        caller=state["caller"],
        callee=state["callee"]
    )
    return {**state, "cdr_data": cdr}


def route_after_cdr(state: AgentState):
    """一次性统一路由：无记录 / 486 / 487 / 5xx / 其他"""
    cdr = state["cdr_data"]
    if cdr.get("msg") == "没有找到对应的通话记录":
        return "no_record"

    code = cdr.get("sip_code", "")
    if code == "486":
        return "sip_486"
    elif code == "487":
        return "sip_487"
    elif code.startswith("5"):
        return "sip_5xx"
    else:
        return "sip_other"


async def fetch_sip_log(state: AgentState) -> AgentState:
    log = await call_sip_log_mcp(call_id=state["call_id"])
    return {**state, "sip_log": log}


async def fetch_prom(state: AgentState) -> AgentState:
    cdr = state["cdr_data"]
    prom = await call_prom_mcp(
        metric="call_error",
        time_start=cdr["start_time"],
        time_end=cdr["end_time"]
    )
    return {**state, "prom_data": prom}


async def gen_busy_report(state: AgentState) -> AgentState:
    cdr = state["cdr_data"]
    text = f"""CDR：{cdr}
结论：SIP 486 USER_BUSY，被叫当前忙线；建议确认被叫是否正在通话。"""
    return {**state, "report": text}


async def gen_timeout_report(state: AgentState) -> AgentState:
    cdr = state["cdr_data"]
    sip_log = state["sip_log"]
    text = f"""CDR：{cdr}
信令日志：{sip_log}
结论：487 请求超时，大概率网络、防火墙、远端未响应。"""
    return {**state, "report": text}


async def gen_5xx_report(state: AgentState) -> AgentState:
    cdr = state["cdr_data"]
    prom = state["prom_data"]
    text = f"""CDR：{cdr}
监控数据：{prom}
结论：5xx 服务端异常，平台侧负载高或服务故障。"""
    return {**state, "report": text}


async def gen_default_report(state: AgentState) -> AgentState:
    cdr = state["cdr_data"]
    ans = await llm.ainvoke(f"根据这条 CDR 生成故障分析：{cdr}")
    return {**state, "report": ans.content}


# ===================== 图组装 =====================
builder = StateGraph(AgentState)
builder.add_node("extract_param", extract_param)
builder.add_node("fetch_cdr", fetch_cdr)
builder.add_node("fetch_sip_log", fetch_sip_log)
builder.add_node("fetch_prom", fetch_prom)
builder.add_node("gen_busy_report", gen_busy_report)
builder.add_node("gen_timeout_report", gen_timeout_report)
builder.add_node("gen_5xx_report", gen_5xx_report)
builder.add_node("gen_default_report", gen_default_report)

builder.add_edge(START, "extract_param")
builder.add_edge("extract_param", "fetch_cdr")

# fetch_cdr 之后一次性分发所有分支
builder.add_conditional_edges(
    "fetch_cdr",
    route_after_cdr,
    {
        "no_record": END,
        "sip_486": "gen_busy_report",
        "sip_487": "fetch_sip_log",
        "sip_5xx": "fetch_prom",
        "sip_other": "gen_default_report"
    }
)

builder.add_edge("fetch_sip_log", "gen_timeout_report")
builder.add_edge("fetch_prom", "gen_5xx_report")

builder.add_edge("gen_busy_report", END)
builder.add_edge("gen_timeout_report", END)
builder.add_edge("gen_5xx_report", END)
builder.add_edge("gen_default_report", END)

graph = builder.compile()


async def run():
    # 测试：abc123 / abc456 / abc789
    result = await graph.ainvoke({
        "user_query": "帮我分析 call_id 是 abc456 的呼叫为什么挂断"
    })
    print("==== 排查报告 ====")
    print(result.get("report", "无报告"))


if __name__ == "__main__":
    asyncio.run(run())
