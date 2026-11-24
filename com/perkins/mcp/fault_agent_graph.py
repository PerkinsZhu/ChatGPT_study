import asyncio
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from mcp_cdr_helper import call_cdr_mcp
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


# 1. 定义状态
class AgentState(TypedDict):
    user_query: str
    call_id: Optional[str]
    caller: Optional[str]
    callee: Optional[str]
    cdr_data: Optional[dict]
    report: Optional[str]


# 2. 模型，改成你自己的地址、key、模型名
llm = ChatOpenAI(
    base_url=os.getenv("base_url", ""),
    api_key=os.getenv("api_key", ""),
    model=os.getenv("model", ""),
)

# 结构化输出定义，让 LLM 稳定提取参数
class ExtractSchema(BaseModel):
    call_id: Optional[str]
    caller: Optional[str]
    callee: Optional[str]


# 节点1：提取参数
async def extract_param(state: AgentState) -> AgentState:
    resp = await llm.with_structured_output(ExtractSchema).ainvoke(state["user_query"])
    return {
        **state,
        "call_id": resp.call_id,
        "caller": resp.caller,
        "callee": resp.callee
    }

# 节点2：调用 MCP 查询 CDR
async def fetch_cdr(state: AgentState) -> AgentState:
    cdr = await call_cdr_mcp(
        call_id=state["call_id"],
        caller=state["caller"],
        callee=state["callee"]
    )
    return {**state, "cdr_data": cdr}

# 节点3：生成故障结论报告
async def gen_report(state: AgentState) -> AgentState:
    cdr = state["cdr_data"]
    prompt = f"""
你是呼叫故障分析专家，根据下面 CDR 信息输出简短故障结论：
{cdr}
要求：说明故障原因、建议排查方向。
"""
    ans = await llm.ainvoke(prompt)
    return {**state, "report": ans.content}

# 分支判断：有没有查到记录
def route_cdr(state: AgentState):
    cdr = state["cdr_data"]
    if cdr.get("msg") == "没有找到对应的通话记录":
        return "no_record"
    return "has_record"


# 组装图
builder = StateGraph(AgentState)
builder.add_node("extract_param", extract_param)
builder.add_node("fetch_cdr", fetch_cdr)
builder.add_node("gen_report", gen_report)

builder.add_edge(START, "extract_param")
builder.add_edge("extract_param", "fetch_cdr")
builder.add_conditional_edges(
    "fetch_cdr",
    route_cdr,
    {
        "has_record": "gen_report",
        "no_record": END
    }
)
builder.add_edge("gen_report", END)

graph = builder.compile()


async def run():
    result = await graph.ainvoke({
        "user_query": "帮我分析 call_id 是 abc123 的呼叫为什么挂断"
    })
    print("==== 最终排查报告 ====")
    print(result.get("report", "未找到通话记录，无法分析"))


if __name__ == "__main__":
    asyncio.run(run())
