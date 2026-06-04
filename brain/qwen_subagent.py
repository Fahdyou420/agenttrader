"""
Qwen dispatch wrapper.
"""
import ollama

with open("prompts/qwen_executor.txt", "r", encoding="utf-8") as f:
    QWEN_SYSTEM_PROMPT = f.read()

def dispatch_to_qwen(task_description: str, context: str) -> str:
    """Dispatch task to Qwen execution engine."""
    messages = [
        {"role": "system", "content": QWEN_SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nTask:\n{task_description}"}
    ]
    
    try:
        response = ollama.chat(
            model="qwen3.5:9b",
            messages=messages
        )
        return response.message.content
    except Exception as e:
        return f"Error executing Qwen task: {str(e)}"
