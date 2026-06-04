"""
Server-Sent Events signal stream for Dashboard.
"""
from flask import Response
import time
import json
import random

def get_signal_stream():
    """Mock SSE stream pushing signals to frontend."""
    def generate():
        while True:
            # Placeholder for pulling from ZMQ or a DB
            time.sleep(10)
            mock_signal = {
                "asset": "XAUUSD",
                "signal": random.choice(["LONG", "SHORT"]),
                "confidence": round(random.uniform(0.75, 0.95), 2),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            yield f"data: {json.dumps(mock_signal)}\n\n"
    
    return Response(generate(), mimetype="text/event-stream")
