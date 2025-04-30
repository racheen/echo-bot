import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "models/embedding-001"
VECTOR_STORE_PATH = "vector_store/"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
