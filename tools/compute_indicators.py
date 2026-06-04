"""Compute technical indicators using pandas-ta."""
import pandas as pd
import pandas_ta as ta
import json

def compute_indicators(ohlc_json: str, indicators: list) -> str:
    """Compute indicators (e.g. ATR, EMA, RSI) from OHLC JSON string."""
    try:
        data = json.loads(ohlc_json)
        if "error" in data:
            return ohlc_json
            
        df = pd.DataFrame(data["data"])
        
        computed = {}
        for ind in indicators:
            ind = ind.lower()
            if ind == "atr":
                df.ta.atr(append=True)
                computed["ATR_14"] = float(df["ATR_14"].iloc[-1]) if "ATR_14" in df else None
            elif ind == "rsi":
                df.ta.rsi(append=True)
                computed["RSI_14"] = float(df["RSI_14"].iloc[-1]) if "RSI_14" in df else None
            elif ind.startswith("ema"):
                length = int(ind.replace("ema", ""))
                df.ta.ema(length=length, append=True)
                col_name = f"EMA_{length}"
                computed[col_name] = float(df[col_name].iloc[-1]) if col_name in df else None
                
        return json.dumps(computed)
    except Exception as e:
        return json.dumps({"error": str(e)})
