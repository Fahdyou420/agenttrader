"""
Flask + HTMX main application.
"""
from flask import Flask, render_template
from dashboard.sse_stream import get_signal_stream

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stream")
def stream():
    return get_signal_stream()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
