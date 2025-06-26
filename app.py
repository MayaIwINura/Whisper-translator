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

# Используй свой ключ в secrets.toml
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

# Стили для всего фона и пузырьков сообщений
st.markdown(
    """
    <style>
    html, body {
      height: 100%;
      margin: 0;
      background: black;
      background: linear-gradient(to top, #4b0082 0%, black 70%);
      color: white;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      overflow-x: hidden;
    }

    .main {
      background: transparent !important;
      padding: 1rem;
    }

    .user-bubble {
        background: linear-gradient(135deg, rgba(147,112,219,0.3), rgba(186,85,211,0.5));
        border-radius: 15px 15px 15px 0px;
        padding: 12px 15px;
        max-width: 70%;
        margin: 6px 0;
        color: white;
        box-shadow:
          0 0 5px 1px rgba(186,85,211,0.6),
          inset 0 0 10px rgba(255,255,255,0.2);
        backdrop-filter: blur(5px);
        float: left;
        clear: both;
    }

    .bot-bubble {
        background: linear-gradient(135deg, rgba(144,238,144,0.3), rgba(60,179,113,0.5));
        border-radius: 15px 15px 0px 15px;
        padding: 12px 15px;
        max-width: 70%;
        margin: 6px 0;
        color: white;
        box-shadow:
          0 0 5px 1px rgba(60,179,113,0.6),
          inset 0 0 10px rgba(255,255,255,0.2);
        backdrop-filter: blur(5px);
        float: right;
        clear: both;
    }

    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main">', unsafe_allow_html=True)

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

def send_message():
    user_text = st.session_state.text_input.strip()
    if not user_text:
        return

    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.spinner("Listening to the soul..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
            )
            gpt_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": gpt_reply})

            save_history(st.session_state.messages)
        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.session_state.text_input = ""

# Текстовое поле с отправкой по Enter
st.text_input("Write your revelation:", key="text_input", on_change=send_message)

# Кнопка отправки с эмоджи (альтернатива)
st.button("💬", on_click=send_message)

# Отображение истории сообщений с пузырьками
if st.session_state.messages:
    st.markdown("---")
    st.subheader("📖 Chat history:")

    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.markdown(f'<div class="user-bubble clearfix">{content}</div>', unsafe_allow_html=True)
        elif role == "assistant":
            st.markdown(f'<div class="bot-bubble clearfix">{content}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
