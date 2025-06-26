import streamlit as st
import openai
import json
import os

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Подключение к OpenAI
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

# Интерфейс
st.title("Whisper Translator")
st.write("Today, you can share what your soul feels.")

# История сообщений
history = load_history()

# Инициализация состояний
if "messages" not in st.session_state:
    st.session_state.messages = history or [
        {
            "role": "system",
            "content": (
                "You are a wise and caring friend, who listens deeply. "
                "You speak kindly and gently, like someone who understands the soul. "
                "You ask thoughtful, open-ended questions that help the user explore their feelings and problems. "
                "Sometimes you share short philosophical insights, but always warmly and supportively. "
                "Make the user feel safe and understood, as if they talk to a close and trusted friend."
            ),
        }
    ]

if "text_handled" not in st.session_state:
    st.session_state.text_handled = False

# Поле ввода
text = st.text_input("Write your revelation:", key="text_input")

# Отправка по кнопке
if st.button("💬") and text.strip():
    st.session_state.messages.append({"role": "user", "content": text})
    st.session_state.text_handled = False
    st.rerun()

# Отправка по Enter
elif text.strip() and not st.session_state.text_handled:
    st.session_state.text_handled = True

    with st.spinner("Listening to the soul..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
            )
            gpt_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": gpt_reply})
            save_history(st.session_state.messages)
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")

# История диалога
st.markdown("---")
st.header("Your chat history:")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Whisper:** {msg['content']}")
