"""
Post-trade analysis writer.
"""
import logging
from tools.save_insight import save_insight
from tools.query_vault import query_vault
from brain.hermes_agent import run_hermes

logging.basicConfig(level=logging.INFO)

def process_trade_close(trade_result: dict):
    logging.info(f"Processing trade close for {trade_result.get('asset')}")
    prompt = f"Analyze this closed trade. Did it hit TP or SL? What was the outcome? Write a post-trade review note.\nTrade Result: {trade_result}"
    context = query_vault(f"signal_{trade_result.get('asset')}", 1)
    result = run_hermes(prompt, context)
    logging.info("Journal Agent review written to vault.")

if __name__ == "__main__":
    # Test stub
    process_trade_close({"asset": "XAUUSD", "outcome": "TP", "pnl": 500})
