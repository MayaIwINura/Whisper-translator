import streamlit as st
import openai
import json
import os

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

# CSS
st.markdown(
    """
    <style>
    body {
      background: linear-gradient(to top, #4b0082 0%, black 90%);
      color: white;
    }
    .bubble-user {
        background-color: rgba(186, 85, 211, 0.25);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin-bottom: 8px;
        width: fit-content;
        max-width: 80%;
        animation: fadeIn 0.3s ease-in-out;
    }
    .bubble-bot {
        background-color: rgba(144, 238, 144, 0.25);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin-bottom: 8px;
        width: fit-content;
        max-width: 80%;
        align-self: flex-end;
        animation: fadeIn 0.3s ease-in-out;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Заголовок
st.title("Whisper Translator")
st.write("Today, you can share what your soul feels.")

# История сообщений
if "messages" not in st.session_state:
    st.session_state.messages = load_history() or [
        {
            "role": "system",
            "content": (
                "You are a wise and caring friend. You respond kindly, ask reflective questions, and help the user go deeper."
            ),
        }
    ]

# Рендер сообщений
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="bubble-bot">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Обработка отправки
def send_message():
    user_input = st.session_state.text_input.strip()
    if user_input == "":
        return
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.text_input = ""
    save_history(st.session_state.messages)

    with st.spinner("Typing..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            save_history(st.session_state.messages)
        except Exception as e:
            st.error(f"Chat error: {e}")

# Поле ввода и кнопка
st.text_input("Write your revelation:", key="text_input", on_change=send_message)
st.button("💬", on_click=send_message)
