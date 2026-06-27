import os
from google import genai
from google.genai import types
from backend.config import settings

# Находим путь к папке с данными (data_pg находится в корне)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data_pg")

# Инициализируем клиента Gemini
client = genai.Client(api_key=settings.gemini_api_key)

def load_knowledge_base() -> str:
    """Читает все .md файлы из папки data_pg и объединяет их в текст."""
    context_parts = []
    
    if not os.path.exists(DATA_DIR):
        return "Контекст пуст. Папка с данными не найдена."
        
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".md"):
            file_path = os.path.join(DATA_DIR, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Добавляем разделитель, чтобы модель понимала, где какая страница
                    context_parts.append(f"--- СТРАНИЦА: {filename} ---\n{content}\n")
            except Exception as e:
                print(f"Ошибка чтения файла {filename}: {e}")
                
    return "\n".join(context_parts)

def get_ai_response(user_message: str) -> str:
    """Отправляет контекст сайта и вопрос пользователя в Gemini."""
    # Собираем контекст из файлов перед каждым запросом (удобно при редактировании .md)
    knowledge_context = load_knowledge_base()
    
    # Системный промпт: задаем поведение и роль бота
    system_instruction = (
        "Ты — официальный ИИ-ассистент платформы Napas Project. "
        "Твоя главная задача — помогать пользователям ориентироваться на сайте, "
        "отвечать на вопросы по правилам, инвентарю, жалобам, банам и функционалу. "
        "Используй ТОЛЬКО предоставленный ниже контекст сайта Napas Project. "
        "Если ответа нет в контексте, вежливо скажи, что не владеешь такой информацией. "
        "Отвечай дружелюбно, четко, структурировано и без лишней 'воды'. "
        "Язык ответа должен соответствовать языку вопроса пользователя (украинский или русский).\n\n"
        f"КОНТЕКСТ САЙТА NAPAS PROJECT:\n{knowledge_context}"
    )
    
    try:
        # Используем быструю и экономичную модель gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,  # Низкая температура, чтобы бот не придумывал лишнего
            )
        )
        return response.text
    except Exception as e:
        print(f"Ошибка при запросе к Gemini API: {e}")
        return "Извините, произошла техническая ошибка. Попробуйте позже."

# Проверка работоспособности движка
if __name__ == "__main__":
    print("Запуск проверки AI движка...")
    test_res = get_ai_response("Привет! Какие правила на проекте?")
    print("\nОтвет бота:\n", test_res)