from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import httpx

app = FastAPI()

# Đọc API key từ biến môi trường
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Định nghĩa kiểu dữ liệu cho tin nhắn
class Message(BaseModel):
    role: str
    content: str

# Định nghĩa kiểu dữ liệu cho request
class ChatRequest(BaseModel):
    messages: list[Message]

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    # Gửi yêu cầu đến OpenRouter
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "X-Title": "VIANN AI"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": m.role, "content": m.content} for m in chat_request.messages],
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=data)
        resp_json = resp.json()
    return resp_json
