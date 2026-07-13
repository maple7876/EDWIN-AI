import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# paths
LOG_DIR = os.path.expanduser("~/KAREN_SYSTEM/LOGS/CHATS")
DB_DIR = os.path.expanduser("~/KAREN_SYSTEM/RAG_DB")

# setup
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection("karen_memory")

model = SentenceTransformer("all-MiniLM-L6-v2")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

for file in os.listdir(LOG_DIR):
    path = os.path.join(LOG_DIR, file)

    try:
        with open(path, "r", errors="ignore") as f:
            text = f.read()

        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            embedding = model.encode(chunk).tolist()

            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[f"{file}_{i}"]
            )

    except Exception as e:
        print("error:", file, e)

print("Memory indexing complete.")
