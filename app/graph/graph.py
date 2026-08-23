from langgraph.graph import StateGraph, START, END
from app.graph.state import RagState
from app.graph.nodes import chat_history, invoke_llm


graph = StateGraph(RagState)

# nodes
graph.add_node('load_history', chat_history.load_history)
graph.add_node('invoke_llm', invoke_llm.invoke_llm)

# edges
graph.add_edge(START, 'load_history')
graph.add_edge('load_history', 'invoke_llm')
graph.add_edge('invoke_llm', END)

# graph compile
chatbot = graph.compile()