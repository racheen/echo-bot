from fastapi import APIRouter
from langchain.schema import HumanMessage, SystemMessage
from app.core.llm_graph import graph
from app.schema.schema import Query

router = APIRouter()

@router.get("/")
async def home():
    return {"success": True}

@router.post("/ask")
async def ask_resume_bot(query: Query):
    messages = []
    for msg in query.messages:
        if msg.sender == "user":
            messages.append(HumanMessage(content=msg.text))
        else:
            messages.append(SystemMessage(content=msg.text))
    state = {"messages": messages, "answer": ""}
    response_state = graph.invoke(state)
    return {"answer": response_state.get("answer", "")}
