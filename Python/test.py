from langgraph.graph import *
from typing import TypedDict

class State(TypedDict):
    count : int

def increment(state: State):
    return {
        "count" : state["count"] + 1
    }
graphBuilder = StateGraph(State)
graphBuilder.add_node("Incrementer", increment)
graphBuilder.add_node("Incrementer_2", increment)
graphBuilder.add_edge(START, "Incrementer")
graphBuilder.add_edge("Incrementer", "Incrementer_2")


graph = graphBuilder.compile()

res = graph.invoke({
    "count" : 1
})

print(res)