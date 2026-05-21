from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.history import HistoryStore
from app.vlm_client import VLMClient, VLMError


VLM_SERVER_URL = os.getenv("VLM_SERVER_URL", "http://172.21.128.209:8000").rstrip("/")
MODEL_NAME = os.getenv("VLM_MODEL_NAME", "")
MAX_TOKENS = int(os.getenv("VLM_MAX_TOKENS", "512"))
SYSTEM_PROMPT = os.getenv("VLM_SYSTEM_PROMPT", "You are a helpful assistant.")
MAX_HISTORY_MESSAGES = int(os.getenv("VLM_MAX_HISTORY", "20"))

app = FastAPI(title="VLM Local Demo")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
history_store = HistoryStore(max_messages=MAX_HISTORY_MESSAGES)
vlm_client = VLMClient(base_url=VLM_SERVER_URL)


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    response: str
    history: List[dict]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    history = history_store.get(req.session_id)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": req.message},
    ]

    try:
        reply = await vlm_client.chat(
            messages=messages,
            model_name=MODEL_NAME or None,
            max_tokens=MAX_TOKENS,
        )
    except VLMError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    history_store.append(req.session_id, {"role": "user", "content": req.message})
    history_store.append(req.session_id, {"role": "assistant", "content": reply})

    return ChatResponse(response=reply, history=history_store.get(req.session_id))


@app.post("/reset")
async def reset(req: ChatRequest) -> dict:
    history_store.clear(req.session_id)
    return {"status": "cleared"}
