"""Tool to query the Obsidian vault."""
from memory.chroma_index import query_vault as query_chroma
import json

def query_vault(query: str, n_results: int = 5) -> str:
    """Query ChromaDB for relevant notes."""
    results = query_chroma(query, n_results)
    if not results:
        return json.dumps({"status": "no results"})
    return json.dumps({"results": results})
