"""
MT5 Real-Time Data Streamer (RUNS ON WINDOWS HOST)
Connects to MetaTrader 5 Terminal running locally on Windows and streams
live quotes (XAUUSD, EURUSD) to the Hermes agent via ZeroMQ.

Note: The MetaTrader5 pip package only supports Windows environments.
Run this natively on Windows 11 host outside of Docker. 
"""
import MetaTrader5 as mt5
import zmq
import time
import json
import logging

logging.basicConfig(level=logging.INFO)

# Configure ZMQ Publisher
# The Docker containers will connect to host.docker.internal:5556
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

def start_stream(symbols=["XAUUSD", "EURUSD"]):
    # Initialize MT5 connection
    if not mt5.initialize():
        logging.error(f"MT5 initialize() failed, error code = {mt5.last_error()}")
        logging.error("Ensure MetaTrader 5 is installed and running on Windows.")
        return
    
    logging.info("Connected to MetaTrader 5.")
    
    # Enable symbols in Market Watch
    for symbol in symbols:
        selected = mt5.symbol_select(symbol, True)
        if not selected:
            logging.warning(f"Failed to select {symbol}")

    logging.info(f"Starting real-time stream for {symbols} on ZMQ port 5556...")
    
    try:
        while True:
            for symbol in symbols:
                tick = mt5.symbol_info_tick(symbol)
                if tick:
                    msg = {
                        "topic": "MARKET_TICK",
                        "symbol": symbol,
                        "time": tick.time,
                        "bid": tick.bid,
                        "ask": tick.ask,
                        "last": tick.last,
                        "volume": tick.volume
                    }
                    # Send multi-part message: [Topic/Symbol] [Data]
                    socket.send_string(f"{symbol} {json.dumps(msg)}")
            time.sleep(0.1) # Poll every 100ms
    except KeyboardInterrupt:
        logging.info("Stopping stream...")
    finally:
        mt5.shutdown()

if __name__ == '__main__':
    start_stream()
