from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from IPython.display import Image

# Step 1: 定义 State
class SimpleState(TypedDict):
    message: str
    processed: bool

# Step 2: 定义节点函数
def greet_node(state: SimpleState) -> dict:
    """欢迎节点：生成问候语"""
    print(f"[greet_node] 收到消息: {state['message']}")
    return {"message": f"你好！{state['message']}"}

def process_node(state: SimpleState) -> dict:
    """处理节点：标记为已处理"""
    print(f"[process_node] 处理消息: {state['message']}")
    return {"processed": True}

def children_node(state: SimpleState) -> dict:
    """处理节点：标记为已处理"""
    print(f"[children_node] 处理消息: {state['message']}")
    return {"children": state['message']+"_children"}


def should_continue(state):
    if state["processed"]:
        return "process"
    else:
        return "children"




# Step 3: 构建图
builder = StateGraph(SimpleState)

# 添加节点
builder.add_node("greet", greet_node)
builder.add_node("process", process_node)
builder.add_node("children", children_node)

# 添加边
builder.add_edge(START, "greet")
# builder.add_edge("greet", "process")
builder.add_conditional_edges(
    "greet",
    should_continue,
    {
        "process": "process",
        "children": "children"
    }
)

builder.add_edge("process", END)
builder.add_edge("children", END)



# Step 4: 编译图
graph = builder.compile()

# Step 5: 运行
result = graph.invoke({
    "message": "世界",
    "processed": False
})

print(f"\n最终结果: {result}")


# 在 Jupyter Notebook 中可视化

Image(graph.get_graph().draw_mermaid_png())

# 或者打印 Mermaid 格式
print(graph.get_graph().draw_mermaid())