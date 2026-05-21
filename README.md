# VLM Local Demo

A minimal chat UI that talks to Qwen via the vLLM HTTP API. This project is standalone and does **not** depend on ROS2 or the `heart1` codebase.

## Features

- FastAPI backend
- Simple chat-style web UI
- Session-based conversation history (in memory)
- Configurable vLLM endpoint and model name

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload
```

Open `http://localhost:7860` in your browser.

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `VLM_SERVER_URL` | `http://172.21.128.209:8000` | vLLM server URL |
| `VLM_MODEL_NAME` | empty | Model name (empty = first model from `/v1/models`) |
| `VLM_MAX_TOKENS` | `512` | Max tokens for response |
| `VLM_SYSTEM_PROMPT` | `You are a helpful assistant.` | System prompt |
| `VLM_MAX_HISTORY` | `20` | Max stored messages per session |

## Notes

- History is stored in memory. Restarting the server clears it.
- This project only uses vLLM's HTTP API.
