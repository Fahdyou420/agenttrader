"""
Main Hermes ReAct Loop and Tool Dispatcher.
"""
import json
import ollama
from brain.tool_registry import TOOLS
from tools.fetch_ohlc import fetch_ohlc
from tools.compute_indicators import compute_indicators
from tools.detect_pattern import detect_pattern
from tools.query_vault import query_vault
from tools.save_insight import save_insight
from tools.emit_signal import emit_signal
from tools.get_news_sentiment import get_news_sentiment
from tools.dispatch_to_qwen import dispatch_to_qwen_tool
from tools.run_backtest import run_backtest

# Load Prompt
with open("prompts/hermes_master.txt", "r", encoding="utf-8") as f:
    HERMES_SYSTEM_PROMPT = f.read()

def parse_signal_json(content: str) -> dict:
    """Parse final JSON output from agent."""
    try:
        # Simplistic parsing, grab json inside the content
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            return json.loads(content[start:end+1])
        return {}
    except Exception:
        return {}

def execute_tool(name: str, arguments: dict):
    """Execute local tools."""
    if name == "fetch_ohlc":
        return fetch_ohlc(**arguments)
    elif name == "compute_indicators":
        return compute_indicators(**arguments)
    elif name == "detect_pattern":
        return detect_pattern(**arguments)
    elif name == "query_vault":
        return query_vault(**arguments)
    elif name == "save_insight":
        return save_insight(**arguments)
    elif name == "emit_signal":
        return emit_signal(**arguments)
    elif name == "get_news_sentiment":
        return get_news_sentiment(**arguments)
    elif name == "dispatch_to_qwen":
        return dispatch_to_qwen_tool(**arguments)
    elif name == "run_backtest":
        return run_backtest(**arguments)
    return f"Tool {name} not found."

def run_hermes(user_message: str, vault_context: str) -> dict:
    """Hermes Master ReAct Loop."""
    try:
        messages = [
            {"role": "system", "content": HERMES_SYSTEM_PROMPT},
            {"role": "user", "content": f"Vault context:\n{vault_context}\n\n{user_message}"}
        ]
        
        while True:
            response = ollama.chat(
                model="hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF:latest",
                messages=messages,
                tools=TOOLS
            )
            
            if not response.message.tool_calls:
                return parse_signal_json(response.message.content)
            
            messages.append(
                {
                    "role": "assistant",
                    "content": response.message.content or "",
                    "tool_calls": response.message.tool_calls
                }
            )
            
            for tc in response.message.tool_calls:
                args = tc.function.arguments
                result = execute_tool(tc.function.name, args)
                messages.append({"role": "tool", "content": str(result), "name": tc.function.name})
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test script
    print("Hermes module initialized.")
