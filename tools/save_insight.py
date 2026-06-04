"""Tool to save insights to the Obsidian vault."""
from memory.vault_manager import write_note
import datetime

def save_insight(title: str, content: str, tags: list, note_type: str) -> str:
    """Save an insight to vault."""
    metadata = {
        "note_type": note_type,
        "tags": tags,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    filename = write_note(title, content, metadata)
    return f"Insight saved as {filename}"
