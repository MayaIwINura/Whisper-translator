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

st.markdown(
    """
    <style>
    html, body {
      height: 100%;
      margin: 0;
      background: white;
      color: #333;
      font-family: 'Inter', sans-serif;
      overflow-x: hidden;
    }

    .main {
      background: transparent !important;
      padding: 1rem;
    }

    @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

    /* Анимация появления */
    @keyframes fadeIn {
      from {opacity: 0; transform: translateY(10px);}
      to {opacity: 1; transform: translateY(0);}
    }

    .message {
      animation: fadeIn 0.5s ease forwards;
    }

    .user-bubble {
        background: #f0f0f0;
        border-radius: 16px 16px 16px 0;
        padding: 12px 15px;
        max-width: 70%;
        margin: 6px 0;
        color: #333;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        float: left;
        clear: both;
    }

    .bot-bubble {
        background: white;
        border-radius: 16px 16px 0 16px;
        padding: 12px 15px;
        max-width: 70%;
        margin: 6px 0;
        color: #333;
        box-shadow: 0 2px 12px rgba(0,0,0,0.15);
        float: right;
        clear: both;
    }

    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }

    button {
        cursor: pointer;
        font-size: 20px;
        padding: 6px 12px;
        border-radius: 12px;
        border: none;
        background-color: #6200EE;
        color: white;
        transition: background-color 0.3s ease;
    }
    button:hover {
        background-color: #3700B3;
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

st.text_input("Write your revelation:", key="text_input", on_change=send_message)

st.button("💬", on_click=send_message)

if st.session_state.messages:
    st.markdown("---")
    st.subheader("📖 Chat history:")

    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.markdown(f'<div class="user-bubble message clearfix">{content}</div>', unsafe_allow_html=True)
        elif role == "assistant":
            st.markdown(f'<div class="bot-bubble message clearfix">{content}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
