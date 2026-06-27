document.addEventListener("DOMContentLoaded", () => {
    // 1. Создаем HTML структуру виджета внутри body
    const chatHTML = `
        <div id="napas-chat-trigger">💬</div>
        <div id="napas-chat-window">
            <div class="napas-chat-header">
                <span>Napas AI Помічник</span>
                <span class="napas-chat-close">&times;</span>
            </div>
            <div class="napas-chat-messages" id="napas-chat-msgs">
                <div class="napas-msg bot">Привіт! Я твій ІИ-помічник Napas Project. Чим можу допомогти? 😊</div>
            </div>
            <div class="napas-chat-input-area">
                <input type="text" id="napas-chat-input" placeholder="Задайте питання..." autocomplete="off">
                <button id="napas-chat-send">▶</button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML("beforeend", chatHTML);

    // 2. Находим элементы управления
    const trigger = document.getElementById("napas-chat-trigger");
    const windowChat = document.getElementById("napas-chat-window");
    const closeBtn = document.querySelector(".napas-chat-close");
    const input = document.getElementById("napas-chat-input");
    const sendBtn = document.getElementById("napas-chat-send");
    const msgsContainer = document.getElementById("napas-chat-msgs");

    // Твой локальный бэкенд на FastAPI
    const API_URL = "http://127.0.0.1:8000/api/chat";

    // Переключение видимости окна чата
    trigger.addEventListener("click", () => {
        windowChat.style.display = windowChat.style.display === "flex" ? "none" : "flex";
        if (windowChat.style.display === "flex") input.focus();
    });

    closeBtn.addEventListener("click", () => {
        windowChat.style.display = "none";
    });

    // Функция отправки сообщения
    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // Добавляем сообщение пользователя на экран
        appendMessage(text, "user");
        input.value = "";

        // Добавляем временную заглушку ожидания ответа бота
        const loadingId = appendMessage("Думаю...", "bot");

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            
            // Удаляем заглушку ожидания и выводим реальный ответ
            document.getElementById(loadingId).remove();
            appendMessage(data.reply, "bot");

        } catch (error) {
            console.error("Помилка зв'язку з бэкендом:", error);
            document.getElementById(loadingId).remove();
            appendMessage("Помилка з'єднання з сервером. Переконайся, что бэкенд запущений.", "bot");
        }
    }

    // Вспомогательная функция отрисовки сообщения
    function appendMessage(text, sender) {
        const msgDiv = document.createElement("div");
        const uniqueId = "msg-" + Date.now();
        msgDiv.id = uniqueId;
        msgDiv.className = `napas-msg ${sender}`;
        msgDiv.innerText = text;
        msgsContainer.appendChild(msgDiv);
        msgsContainer.scrollTop = msgsContainer.scrollHeight; // Скролл вниз
        return uniqueId;
    }

    // Обработчики клика и нажатия Enter
    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});