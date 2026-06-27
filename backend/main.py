import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.ai_engine import get_ai_response
from backend.config import settings

app = FastAPI(title="Napas Project AI Bot MVP")

# Настройка CORS, чтобы наш виджет (даже запущенный из файла) мог общаться с бэкендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для MVP разрешаем запросы отовсюду
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Схема входящего запроса от фронтенда
class ChatRequest(BaseModel):
    message: str

# Схема ответа бэкенда
class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Эндпоинт, куда фронтенд отправляет сообщения пользователя."""
    ai_reply = get_ai_response(request.message)
    return ChatResponse(reply=ai_reply)

@app.get("/health")
async def health_check():
    """Простая проверка, что сервер жив."""
    return {"status": "ok"}

if __name__ == "__main__":
    # Запуск сервера uvicorn на хосте и порту из .env
    uvicorn.run(
        "backend.main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=True  # reload=True автоматически перезапускает сервер при изменении кода
    )