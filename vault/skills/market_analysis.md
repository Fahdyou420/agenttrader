---
name: market-analysis
description: Autonomous market structure and sentiment analysis skill
version: "1.0.0"
note_type: skill
---

# Market Analysis Skill

## Trigger Conditions
Activate when the user asks me to "analyze the market", "get market sentiment", "review historical patterns" or when scheduled by cron for daily pre-session prep.

## Rules

### 1. Data Intake
- Call `fetch_ohlc(symbol, timeframe="H1", bars=50)` for the target symbol (e.g., XAUUSD).
- Call `get_news_sentiment(symbol, lookback_hours=24)` to fetch recent NLP sentiment scores.
- Call `query_vault(query="similar historical setups for {symbol}")` to invoke cross-session memory and retrieve prior failed or successful setups from ChromaDB.

### 2. Reasoning Engine (Hermes-3-Llama-3.1-8B-GGUF)
- Isolate the structural constraints (SMC): Look for liquidity sweeps, fair value gaps (FVG), and order blocks (OB).
- Compare structural technicals with fundamental sentiment. Identify *conflicting signals* (e.g., bearish price action but highly bullish news sentiment).
- Reference the retrieved vault context: Have we traded this exact paradigm before? What was the outcome?

### 3. Output Format
Produce a structured markdown analysis and use the `save_insight` tool to record it automatically to the vault.

```markdown
# Market Analysis: {Symbol}
**Timestamp**: {Time}
**Session**: {London/NY/Asia}
**News Sentiment Score**: {VADER score, e.g., 0.65}

## Price Action Insights
- **Key Liquidity Levels**: [Identify sweeps/targets]
- **Volatility (ATR)**: [State current ATR expansion/contraction]

## Vault Recall
- [Insert retrieved context from past trades in this regime]

## Synthesis (Hermes)
[Combined synthesis detailing market probability and direction]
```

## Constraints
- **Do not emit a trade signal from this skill directly.** This skill is exclusively for analysis and state-building.
- Always use `save_insight` with `note_type: market_observation` so the Signal Agent can easily pull this context during its M5 loop.
