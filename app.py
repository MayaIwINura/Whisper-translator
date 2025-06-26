import streamlit as st
import openai
import json
import os

if "text_input" not in st.session_state:
    st.session_state.text_input = ""
    

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

st.title("Whisper Translator")
st.write("Today, you can share what your soul feels.")

if "messages" not in st.session_state:
    st.session_state.messages = load_history() or [
        {
            "role": "system",
            "content": (
                "You are a wise and caring friend, who listens deeply. "
                "You speak kindly and gently, like someone who understands the soul. "
                "You ask thoughtful, open-ended questions that help the user explore their feelings and problems. "
                "Sometimes you share short philosophical insights, but always warmly and supportively."
            ),
        }
    ]

if "text_handled" not in st.session_state:
    st.session_state.text_handled = False

if "last_bot_reply" not in st.session_state:
    st.session_state.last_bot_reply = ""

# Связываем input с session_state для очистки
text = st.text_input("Write your revelation:", key="text_input")

# Функция для отправки сообщения
def send_message(user_text):
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.spinner("Listening to the soul..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
            )
            gpt_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": gpt_reply})
            st.session_state.last_bot_reply = gpt_reply

            save_history(st.session_state.messages)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Отправка по кнопке
if st.button("💬") and text.strip():
    send_message(text)
    st.session_state.text_input = ""  # очищаем поле после отправки
    st.session_state.text_handled = False
    st.rerun()

# Отправка по Enter
elif text.strip() and not st.session_state.text_handled:
    st.session_state.text_handled = True
    send_message(text)
    st.session_state.text_input = ""  # очищаем поле
    st.rerun()

# Показываем последний ответ Whisper (без повтора твоего сообщения)
if st.session_state.last_bot_reply:
    st.markdown("---")
    st.subheader("🪶 Whisper responds:")
    st.markdown(st.session_state.last_bot_reply)

# Показываем всю историю
if st.session_state.messages:
    st.markdown("---")
    st.subheader("📖 Full chat history:")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Whisper:** {msg['content']}")
