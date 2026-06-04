"""ZMQ signal sender to MT5."""
import zmq
import json
import os
from bridge.risk_sizer import get_balance, risk_sizer
from tools.save_insight import save_insight
import datetime

ZMQ_PORT = os.environ.get("ZMQ_PORT", "5555")

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect(f"tcp://localhost:{ZMQ_PORT}")

def emit_signal(signal_json: str) -> str:
    """Send signal to MT5 over ZMQ."""
    try:
        if isinstance(signal_json, str):
            signal = json.loads(signal_json)
        else:
            signal = signal_json
            
        # Validate before sending
        assert float(signal.get("rr", 0)) >= 1.5, "RR below minimum"
        assert float(signal.get("confidence", 0)) >= 0.72, "Confidence below threshold"
        
        # Determine SL pips (mock calculation)
        entry = float(signal.get("entry", 0))
        sl = float(signal.get("sl", 0))
        sl_pips = abs(entry - sl) * 10 # roughly for gold, adapt logic per asset
        
        lot = risk_sizer(balance=get_balance(), risk_pct=0.01, sl_pips=sl_pips)
        signal["lot"] = lot
        
        if "timestamp" not in signal:
            signal["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
        socket.send_json(signal)
        
        # Save to vault
        save_insight(
            title=f"signal_{signal.get('asset')}_{signal.get('timestamp')}",
            content=json.dumps(signal, indent=2),
            tags=["signal", signal.get('asset', ''), signal.get('timeframe', '')],
            note_type="signal"
        )
        
        return "Signal emitted and saved successfully."
    except Exception as e:
        return f"Error emitting signal: {str(e)}"
