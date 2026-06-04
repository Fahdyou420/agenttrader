"""
Weekly accuracy calibration.
"""
from brain.hermes_agent import run_hermes
from tools.query_vault import query_vault
import logging

logging.basicConfig(level=logging.INFO)

def run_calibration():
    logging.info("Starting weekly calibration...")
    prompt = "Compile accuracy breakdown by pattern type. Read signals and journals. Update CALIBRATION.md via save_insight."
    context = query_vault("all signals and journals from past 90 days", 10)
    result = run_hermes(prompt, context)
    logging.info(f"Calibration completed: {result}")

if __name__ == "__main__":
    run_calibration()
