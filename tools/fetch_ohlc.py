"""Fetch OHLC data for given symbol."""
import yfinance as yf
import pandas as pd
import json

def fetch_ohlc(symbol: str, timeframe: str, bars: int = 200) -> str:
    """Fetch OHLC bars using yfinance (simplified alternative to ccxt for now)."""
    try:
        if symbol == "XAUUSD":
            symbol = "GC=F" # Gold futures as a rough proxy on yfinance for XAUUSD
        elif "USD" in symbol and len(symbol) == 6:
            symbol = f"{symbol[:3]}{symbol[3:]}=X" # e.g. EURUSD=X
            
        # mapping M15 etc to yfinance intervals
        # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        interval_map = {"M1": "1m", "M5": "5m", "M15": "15m", "H1": "1h", "D1": "1d"}
        interval = interval_map.get(timeframe.upper(), "15m")
        
        df = yf.download(symbol, interval=interval, period="1mo", progress=False)
        if df.empty:
            return json.dumps({"error": f"No data found for {symbol}"})
        
        df = df.tail(bars)
        df.reset_index(inplace=True)
        # Handle multi-index columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        data = []
        for _, row in df.iterrows():
            date_val = row.get("Datetime", row.get("Date", ""))
            data.append({
                "timestamp": str(date_val),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": float(row["Volume"]) if "Volume" in df else 0.0
            })
        return json.dumps({"symbol": symbol, "timeframe": timeframe, "data": data})
    except Exception as e:
        return json.dumps({"error": str(e)})
