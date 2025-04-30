from pydantic import BaseModel
from typing import List, Literal

# Define LangGraph state and chatbot logic
class ResumeState(dict):
    messages: list  # list of LangChain messages
    answer: str     # most recent response

class Message(BaseModel):
    sender: Literal['user', 'bot']
    text: str

class Query(BaseModel):
    messages: List[Message]
