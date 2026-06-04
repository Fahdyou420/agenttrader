# HERMES Deployment Guide: Windows 11 Local

This guide explains how to properly deploy and initialize the Autonomous Trading Intelligence System on a local Windows 11 machine using Docker Compose, WSL2, and native Windows Python for the MetaTrader 5 connection.

Because the system relies on native Windows interaction for MetaTrader 5 and GPU-accelerated local Ollama, the deployment is split across host-native elements and isolated Docker containers.

---

## Step 1: Prepare MetaTrader 5 on Windows Host
The `MetaTrader5` Python package relies on Windows DLLs and natively injected memory mappings. **It cannot run in Linux Docker containers.**
1. Install MetaTrader 5 on Windows.
2. Log into your FTMO or broker account. Make sure Auto-Trading is enabled.
3. Open a Windows PowerShell/CMD terminal.
4. Install the required Python dependencies natively for the bridge:
   ```bash
   pip install MetaTrader5 pyzmq
   ```
5. Run the MT5 data streamer on your Windows host:
   ```bash
   python bridge/mt5_streamer.py
   ```
   *This opens a ZeroMQ PUB socket on port `5556` that the Docker containers will subscribe to.*

---

## Step 2: Prepare Local Ollama (Windows Host)
To leverage your local NVIDIA RTX 4060 effectively, Ollama runs natively on the Windows Host.
1. Download and run [Ollama for Windows](https://ollama.com).
2. Pull the required models as specified in `config/models.yaml`:
   ```bash
   ollama pull hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF:latest
   ollama pull qwen3.5:9b
   ollama pull nomic-embed-text:latest
   ```

*Note: The Docker containers are pre-configured to connect to `host.docker.internal:11434` to access this native host Ollama instance.*

---

## Step 3: Configure Environment
Ensure your `.env` file matches your local environment setup. It should already be correctly scaffolded:
```env
VAULT_PATH=./vault
CHROMA_PATH=./chroma_db
ZMQ_PORT=5555
OLLAMA_HOST=host.docker.internal:11434
```

---

## Step 4: Deploy the Hermes AI Stack via Docker
With MT5 streaming data natively and Ollama hosting the models natively, we spin up the orchestration, memory databases, and Dashboards inside Docker.
1. Open a terminal in this project's root folder.
2. Build and launch the container stack:
   ```bash
   docker-compose up --build -d
   ```

### What happens now?
- **ChromaDB** starts as an isolated vector store.
- **hermes-brain** runs as an agent daemon, monitoring data, processing R&D, and maintaining the memory layer.
- **signal-scheduler** and **rd-agent** initiate background cron jobs to check markets periodically.
- **dashboard** runs a lightweight Flask/HTMX interface for signal visibility.

## Step 5: Access the Dashboard
Open your brower and navigate to:
`http://localhost:5000`

The dashboard uses Server-Sent Events (SSE) to live-update when Hermes issues trade commands. 

## Daily Operations & Skills
Because this agent uses **Harness Engineering**, its knowledge evolves. 
- You can find its memory and skills in the `./vault` folder (mounted from Docker to your Windows host).
- Check the newly generated `/vault/skills/market_analysis.md` skill to see how Hermes automatically incorporates SMC principles and text-sentiment into pre-trade routines.
