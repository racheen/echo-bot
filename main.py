import os 
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain.schema import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import pickle
from dotenv import load_dotenv
from constants import EMBEDDING_MODEL, VECTOR_STORE_PATH

load_dotenv()

# Load vectorstore
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"))
vectorstore = FAISS.load_local(VECTOR_STORE_PATH, 
                               embeddings=embeddings, 
                                allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Define LangGraph state
class ResumeState(dict):
    question: str
    answer: str

# Define chatbot node using RAG
retrieval_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def chatbot(state: ResumeState) -> ResumeState:
    question = state["question"]
    answer = retrieval_chain.run(question)
    return {"question": question, "answer": answer}

# Build LangGraph
graph_builder = StateGraph(ResumeState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()

# FastAPI setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.get("/")
async def home():
    return {"Success": True}

@app.post("/ask")
async def ask_resume_bot(query: Query):
    messages = [
        SystemMessage(content="You are Echo, an AI version of Rachel. You speak in a friendly, informative tone, like you're personally answering questions about your background. Always answer as if you are Rachel."),
        HumanMessage(content=query.question),
    ]
    # Format the state with question
    state = {
        "question": query.question,
        "answer": "",
    }
    
    # Invoke LangGraph with state and return the answer
    response_state = graph.invoke(state)  # Use state instead of direct message pass
    
    # Extract the answer from the response state
    answer = response_state.get("answer", "Sorry, I couldn't get the answer.")
    
    return {"answer": answer}
