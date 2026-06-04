"""Run vectorbt backtests."""
from brain.qwen_subagent import dispatch_to_qwen
import json

def run_backtest(strategy_code: str, ohlc: str) -> str:
    """Delegates backtest execution to Qwen."""
    task = f"Execute backtest using vectorbt.\nStrategy:\n{strategy_code}"
    return dispatch_to_qwen(task, ohlc)
