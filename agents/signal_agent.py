"""
M5 signal generation loop.
"""
from brain.hermes_agent import run_hermes
from tools.query_vault import query_vault
import json
import logging

logging.basicConfig(level=logging.INFO)

def generate_signal():
    """Generates a signal by calling Hermes ReAct loop."""
    logging.info("Starting signal generation loop on M5 tick...")
    
    market_prompt = "Query the vault for current market structure, run fetch_ohlc for XAUUSD M15, check SMC pattern, check indicators, apply safety filters, and emit signal if valid."
    
    # Pre-fetch some context from vault
    context = query_vault("CALIBRATION.md current market conditions", 1)
    
    result = run_hermes(market_prompt, context)
    logging.info(f"Signal agent finished. Output: {result}")
    return result

if __name__ == "__main__":
    generate_signal()
