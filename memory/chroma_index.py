"""
ChromaDB Indexer Module
Embed + upsert + search ChromaDB
"""
import os
import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = os.environ.get("CHROMA_PATH", "./chroma_db")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# Add a prefix if the host doesn't have http schema
if not OLLAMA_HOST.startswith("http"):
    OLLAMA_HOST = f"http://{OLLAMA_HOST}"

client = chromadb.PersistentClient(path=CHROMA_PATH)

ef = embedding_functions.OllamaEmbeddingFunction(
    url=f"{OLLAMA_HOST}/api/embeddings",
    model_name="nomic-embed-text"
)

collection = client.get_or_create_collection("vault", embedding_function=ef)

def index_note(note_id: str, content: str, metadata: dict):
    """Upserts a note into the ChromaDB vector store."""
    valid_metadata = {k: str(v) for k, v in metadata.items() if v is not None}
    collection.upsert(
        ids=[note_id],
        documents=[content],
        metadatas=[valid_metadata]
    )

def query_vault(query: str, n_results: int = 5) -> list:
    """Queries ChromaDB by semantic similarity."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    if not results or "documents" not in results or not results["documents"]:
        return []
    return results["documents"][0]
