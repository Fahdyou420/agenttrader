"""FTMO-safe ATR-based lot calculation."""

def get_balance() -> float:
    """Mock get balance."""
    return 100000.0

def risk_sizer(balance: float, risk_pct: float, sl_pips: float) -> float:
    """Calculate lot size based on risk per trade and stop loss pips."""
    if sl_pips <= 0:
        return 0.01
    risk_amount = balance * risk_pct
    # Assuming $10 per pip for 1 standard lot
    pip_value_per_lot = 10.0
    lot_size = risk_amount / (sl_pips * pip_value_per_lot)
    return round(lot_size, 2)
