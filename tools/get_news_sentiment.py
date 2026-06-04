"""Get news sentiment for symbol."""
import json
import random

def get_news_sentiment(symbol: str, lookback_hours: int = 24) -> str:
    """Gets RSS feed sentiment using generic VADER/TextBlob mock for now."""
    # Simplified placeholder
    return json.dumps({
        "symbol": symbol,
        "sentiment_score": round(random.uniform(-1, 1), 2),
        "impact": "moderate",
        "lookback_hours": lookback_hours
    })
