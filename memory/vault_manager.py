"""
Vault Manager Module
Handles reading and writing Obsidian .md files with YAML frontmatter.
"""
import os
import datetime
import frontmatter
from memory.chroma_index import index_note

VAULT_PATH = os.environ.get("VAULT_PATH", "/vault")

def get_vault_path(note_type: str) -> str:
    """Generate sub-directory path based on note type."""
    type_to_dir = {
        "signal": "signals",
        "journal": "journal",
        "lesson": "lessons",
        "hypothesis": "rd_hypotheses",
        "backtest": "backtest",
        "market_observation": "market_obs",
        "R&D": "strategies",
    }
    sub_dir = type_to_dir.get(note_type, "system")
    return os.path.join(VAULT_PATH, sub_dir)

def write_note(title: str, content: str, metadata: dict) -> str:
    """
    Writes a markdown file with YAML frontmatter to the Obsidian vault.
    Suffixes filename if it already exists.
    """
    note_type = metadata.get("note_type", "market_observation")
    target_dir = get_vault_path(note_type)
    os.makedirs(target_dir, exist_ok=True)
    
    base_filename = title.replace(" ", "_").replace("/", "_")
    filename = f"{base_filename}.md"
    file_path = os.path.join(target_dir, filename)
    
    counter = 2
    while os.path.exists(file_path):
        filename = f"{base_filename}_v{counter}.md"
        file_path = os.path.join(target_dir, filename)
        counter += 1
        
    post = frontmatter.Post(content, **metadata)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
        
    print(f"Saved to vault: {file_path}")
    # After writing to vault, immediately update chroma index
    index_note(filename, content, metadata)
    return filename

def read_note(filename: str) -> dict:
    """Reads a markdown file with frontmatter from the vault."""
    for root, _, files in os.walk(VAULT_PATH):
        if filename in files:
            path = os.path.join(root, filename)
            post = frontmatter.load(path)
            return {"metadata": post.metadata, "content": post.content}
    return {}
