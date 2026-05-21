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

---

# VLM Local Demo 日本語版

vLLM HTTP API 経由で Qwen と通信する、最小構成のチャット UI です。このプロジェクトは単体で動作し、ROS2 や `heart1` コードベースには依存しません。

## 機能

- FastAPI バックエンド
- シンプルなチャット形式の Web UI
- セッションごとの会話履歴保存（メモリ上）
- vLLM エンドポイントとモデル名の設定

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

conda 環境を使う場合:

```bash
conda create -n qwen-local-demo python=3.11 -y
conda activate qwen-local-demo
pip install -r requirements.txt
```

## 起動

```bash
uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload
```

ブラウザで `http://localhost:7860` を開いてください。

vLLM サーバーの URL を指定する場合:

```bash
export VLM_SERVER_URL=http://172.21.128.209:8000
uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload
```

## 環境変数

| 変数 | デフォルト | 説明 |
| --- | --- | --- |
| `VLM_SERVER_URL` | `http://172.21.128.209:8000` | vLLM サーバーの URL |
| `VLM_MODEL_NAME` | 空 | モデル名（空の場合は `/v1/models` の最初のモデルを使用） |
| `VLM_MAX_TOKENS` | `512` | 応答の最大トークン数 |
| `VLM_SYSTEM_PROMPT` | `You are a helpful assistant.` | システムプロンプト |
| `VLM_MAX_HISTORY` | `20` | セッションごとに保存する最大メッセージ数 |

## 注意点

- 履歴はメモリ上に保存されます。サーバーを再起動すると履歴は消えます。
- このプロジェクトは vLLM の HTTP API のみを使用します。
- Qwen/vLLM サーバー本体はこのプロジェクトには含まれていません。別途 `/v1/models` と `/v1/chat/completions` を提供する vLLM サーバーを起動しておく必要があります。
