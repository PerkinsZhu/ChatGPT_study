import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

client = OpenAI(
    base_url=os.getenv("base_url", ""),
    api_key=os.getenv("api_key", "")
)


# 模拟 CDR 工具，你后面替换成真实 HTTP 调用 ES/MySQL
def query_cdr(call_id: str | None = None, caller: str | None = None, callee: str | None = None,
              time_start: str | None = None, time_end: str | None = None):
    """
    查询通话 CDR 记录
    :param call_id: 呼叫唯一ID
    :param caller: 主叫号码
    :param callee: 被叫号码
    :param time_start: 起始时间，格式 2026-11-24 10:00:00
    :param time_end: 结束时间
    """
    # 这里替换成你真实业务接口
    if call_id == "abc123":
        return {
            "call_id": "abc123",
            "sip_code": "486",
            "hangup_cause": "USER_BUSY",
            "start_time": "2026-11-24 10:05:00",
            "end_time": "2026-11-24 10:05:03"
        }
    return {"msg": "没有找到对应的通话记录"}


tools = [
    {
        "type": "function",
        "function": {
            "name": "query_cdr",
            "description": "根据call_id、主被叫、时间范围查询通话CDR，获取SIP响应码、挂机原因",
            "parameters": {
                "type": "object",
                "properties": {
                    "call_id": {"type": "string", "description": "呼叫ID"},
                    "caller": {"type": "string", "description": "主叫号码"},
                    "callee": {"type": "string", "description": "被叫号码"},
                    "time_start": {"type": "string"},
                    "time_end": {"type": "string"}
                },
                "required": []
            }
        }
    }
]

tool_map = {
    "query_cdr": query_cdr
}


def run_react_agent(user_input: str):
    messages = [{"role": "user", "content": user_input}]
    max_loop = 2
    for _ in range(max_loop):
        resp = client.chat.completions.create(
            model="gpt-6.1-sol",
            messages=messages,
            tools=tools
        )
        msg = resp.choices[0].message
        messages.append(msg)

        # 模型不需要调用工具，直接输出答案，结束循环
        if not msg.tool_calls:
            return msg.content

        # 执行工具
        for tc in msg.tool_calls:
            func_name = tc.function.name
            args = json.loads(tc.function.arguments)
            result = tool_map[func_name](**args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False)
            })
    return "达到最大轮次，排查终止"


if __name__ == "__main__":
    print(run_react_agent("帮我查 call_id abc123 为什么挂断"))
