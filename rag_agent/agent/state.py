from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage

def add_messages(left, right):
    return left + right

class AgentState(TypedDict):
    question: str
    retrieved_data: str
    analysis_result: str
    final_answer: str
    messages: Annotated[List[BaseMessage], add_messages]