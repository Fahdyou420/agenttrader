"""Tool schemas for Ollama ReAct loop."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "fetch_ohlc",
            "description": "Fetch OHLC bars for a symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "timeframe": {"type": "string"},
                    "bars": {"type": "integer", "default": 200}
                },
                "required": ["symbol", "timeframe"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compute_indicators",
            "description": "Compute indicators like ATR, EMA, RSI",
            "parameters": {
                "type": "object",
                "properties": {
                    "ohlc_json": {"type": "string", "description": "JSON string of OHLC data"},
                    "indicators": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["ohlc_json", "indicators"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "detect_pattern",
            "description": "Detect SMC patterns (CHoCH, BOS, OB, FVG)",
            "parameters": {
                "type": "object",
                "properties": {
                    "ohlc_json": {"type": "string"},
                    "pattern_type": {"type": "string"}
                },
                "required": ["ohlc_json", "pattern_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_vault",
            "description": "Query Obsidian vault using semantic search",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "n_results": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_insight",
            "description": "Save a note to the Obsidian vault",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "note_type": {"type": "string"}
                },
                "required": ["title", "content", "tags", "note_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "emit_signal",
            "description": "Send a trade signal to execution bridge",
            "parameters": {
                "type": "object",
                "properties": {
                    "signal_json": {"type": "string", "description": "JSON string of the signal"}
                },
                "required": ["signal_json"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_news_sentiment",
            "description": "Get news sentiment for symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "lookback_hours": {"type": "integer", "default": 24}
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dispatch_to_qwen",
            "description": "Dispatch task to Qwen execution engine",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_description": {"type": "string"},
                    "context": {"type": "string"}
                },
                "required": ["task_description", "context"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_backtest",
            "description": "Run vectorbt backtest strategy",
            "parameters": {
                "type": "object",
                "properties": {
                    "strategy_code": {"type": "string"},
                    "ohlc": {"type": "string"}
                },
                "required": ["strategy_code", "ohlc"]
            }
        }
    }
]
