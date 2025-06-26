import streamlit as st
import openai
import json
import os

st.set_page_config(page_title="Whisper Translator", layout="centered")

# 🔑 API-ключ из секрета
openai.api_key = st.secrets["openai_api_key"]
client = openai.OpenAI(api_key=openai.api_key)

# Путь к файлу истории
HISTORY_FILE = "chat_history.json"

# Загрузка истории
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# Сохранение истории
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Инициализация истории в сессии
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# 💅 Стилизация
st.markdown("""
<style>
body {
    background: linear-gradient(to top, #4b0082 0%, black 90%);
    color: white;
}
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.bubble-user {
    background-color: rgba(186, 85, 211, 0.25); /* сиреневый */
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    width: fit-content;
    max-width: 80%;
    animation: fadeIn 0.6s ease-in-out;
}
.bubble-bot {
    background-color: rgba(173, 216, 230, 0.25); /* голубой */
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    width: fit-content;
    max-width: 80%;
    align-self: flex-end;
    animation: fadeIn 0.6s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
/* Кнопка */
button[kind="secondaryFormSubmit"] {
    animation: glowButton 5s infinite ease-in-out;
    border: none;
    background-color: transparent;
    font-size: 24px;
    transition: transform 0.2s;
}
button[kind="secondaryFormSubmit"]:hover {
    transform: scale(1.1);
}
@keyframes glowButton {
    0% { text-shadow: 0 0 4px rgba(255,255,255,0.2); }
    50% { text-shadow: 0 0 12px rgba(255,255,255,0.5); }
    100% { text-shadow: 0 0 4px rgba(255,255,255,0.2); }
}
/* Лунный индикатор */
.typing-indicator {
    font-size: 22px;
    margin: 20px 0;
    text-align: center;
    animation: moonCycle 2s infinite steps(8);
}
@keyframes moonCycle {
    0% { content: "🌑"; }
    12% { content: "🌒"; }
    25% { content: "🌓"; }
    37% { content: "🌔"; }
    50% { content: "🌕"; }
    62% { content: "🌖"; }
    75% { content: "🌗"; }
    87% { content: "🌘"; }
    100% { content: "🌑"; }
}
</style>
""", unsafe_allow_html=True)

# 🧠 Название и подзаголовок
st.title("Whisper Translator")
st.write("Today, you can share what your soul feels.")

# 📜 Отображение истории
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        bubble_class = "bubble-user" if role == "user" else "bubble-bot"
        st.markdown(f'<div class="{bubble_class}">{content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 📝 Ввод формы
form = st.form(key="chat_form", clear_on_submit=True)
user_input = form.text_input("Write your revelation:", key="text_input", label_visibility="collapsed")
submit = form.form_submit_button("💬")

# 💬 Обработка отправки
if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_history(st.session_state.messages)

    # 🌙 Имитируем "написание"
    placeholder = st.empty()
    placeholder.markdown('<div class="typing-indicator">🌑 Thinking...</div>', unsafe_allow_html=True)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        save_history(st.session_state.messages)
    finally:
        placeholder.empty()
