"""
Python <-> MT5 ZeroMQ bridge.
"""
import zmq
import json
import logging
import os

logging.basicConfig(level=logging.INFO)
ZMQ_PORT = os.environ.get("ZMQ_PORT", "5555")

def start_bridge():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind(f"tcp://*:{ZMQ_PORT}")
    
    logging.info(f"ZMQ Bridge listening on port {ZMQ_PORT}...")
    
    while True:
        try:
            message = socket.recv_json()
            logging.info(f"Received signal from Hermes: {json.dumps(message, indent=2)}")
            # In a real scenario, we'll send it via another socket to MT5 EA
            # For now, it just prints it out as the receiver simulation
        except Exception as e:
            logging.error(f"Error receiving message: {e}")

if __name__ == "__main__":
    start_bridge()
