import os
import json
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from constants import EMBEDDING_MODEL, DOCUMENTS_PATH, VECTOR_STORE_PATH

load_dotenv()

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(text)


# Load all .txt files from the directory
txt_loader = DirectoryLoader(
    DOCUMENTS_PATH,
    glob="**/*.txt",
    loader_cls=TextLoader
)
txt_docs = txt_loader.load()

# Load all .json files manually
json_docs = []
for filename in os.listdir(DOCUMENTS_PATH):
    if filename.endswith(".json"):
        filepath = os.path.join(DOCUMENTS_PATH, filename)
        with open(filepath, "r") as f:
            data = json.load(f)
            # Try to extract meaningful text from known keys; fallback to dumping
            content = (
                data.get("description") or
                data.get("text") or
                json.dumps(data, indent=2)
            )
            json_docs.append(Document(page_content=content, metadata={"source": filename}))

# 3. Combine all documents
all_docs = txt_docs + json_docs
docs = chunk_text(all_docs) 

embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"))
vectorstore = FAISS.from_documents(docs, embeddings)

# To save
vectorstore.save_local(VECTOR_STORE_PATH)