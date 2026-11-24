from langgraph.graph import StateGraph, END
from typing import TypedDict

# 1. 定义状态
class State(TypedDict):
    input: str
    output: str

# 2. 定义节点函数
def node1(state: State):
    return {"output": f"处理：{state['input']}"}

# 3. 建图
builder = StateGraph(State)
builder.add_node("node1", node1)
builder.set_entry_point("node1")
builder.add_edge("node1", END)

# def should_continue(state):
#     if len(state["output"]) > 100:
#         return "end"
#     else:
#         return "more"
#
# builder.add_conditional_edges(
#     "node1",
#     should_continue,
#     {
#         "more": "node2",
#         "end": END
#     }
# )

# 4. 编译运行
graph = builder.compile()
result = graph.invoke({"input": "hello"})
print(result)