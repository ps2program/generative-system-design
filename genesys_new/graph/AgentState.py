from typing import Annotated, Sequence, TypedDict, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # Messages contain the conversation history
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Response schema for additional context and metadata
    response_schema: Annotated[Dict[str, Any], "Schema for the response content"]
    
    # Question type for categorizing the question
    questionType: Annotated[str, "Type of the question"]
