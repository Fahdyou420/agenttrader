"""
Daily R&D hypothesis generation + backtest loop.
"""
from brain.hermes_agent import run_hermes
from tools.query_vault import query_vault
import logging

logging.basicConfig(level=logging.INFO)

def run_rd_cycle():
    logging.info("Starting R&D Cycle...")
    prompt = "Query vault for past 30 days backtests and lessons. Generate 3 new strategy hypotheses for underperforming patterns. Use dispatch_to_qwen to backtest each. Ingest results."
    context = query_vault("lessons and backtests from past 30 days", 5)
    result = run_hermes(prompt, context)
    logging.info(f"R&D Agent output: {result}")

if __name__ == "__main__":
    run_rd_cycle()
