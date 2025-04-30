from langchain.schema import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langgraph.graph import StateGraph
from app.schema.schema import ResumeState
from app.core.config import EMBEDDING_MODEL, VECTOR_STORE_PATH, GOOGLE_API_KEY

# Embeddings + vector store
embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=GOOGLE_API_KEY
)
vectorstore = FAISS.load_local(
    VECTOR_STORE_PATH,
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# LangGraph logic
def chatbot(state: ResumeState) -> ResumeState:
    messages = state["messages"]
    latest_question = messages[-1].content
    rag_answer = rag_chain.run(latest_question)
    ai_response = HumanMessage(content=rag_answer)

    return {
        "messages": messages + [ai_response],
        "answer": rag_answer
    }

# Graph init
graph_builder = StateGraph(ResumeState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()
