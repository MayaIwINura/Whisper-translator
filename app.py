import streamlit as st
import openai
import json
import os
import time

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

    /* Плавное появление */
    @keyframes fadeIn {
      from {opacity: 0; transform: translateY(10px);}
      to {opacity: 1; transform: translateY(0);}
    }

    /* Мерцание */
    @keyframes glow {
      0%, 100% {
        box-shadow: 0 0 5px 2px rgba(255,255,255,0.3);
      }
      50% {
        box-shadow: 0 0 15px 6px rgba(255,255,255,0.7);
      }
    }

    /* Анимация трёх точек */
    .typing-indicator::after {
      content: '...';
      animation: dots 1.5s steps(5, end) infinite;
      font-weight: bold;
      margin-left: 4px;
    }
    @keyframes dots {
      0%, 20% {
        color: rgba(255,255,255,0);
        text-shadow:
          .25em 0 0 rgba(255,255,255,0),
          .5em 0 0 rgba(255,255,255,0);
      }
      40% {
        color: white;
        text-shadow:
          .25em 0 0 rgba(255,255,255,0),
          .5em 0 0 rgba(255,255,255,0);
      }
      60% {
        text-shadow:
          .25em 0 0 white,
          .5em 0 0 rgba(255,255,255,0);
      }
      80%, 100% {
        text-shadow:
          .25em 0 0 white,
          .5em 0 0 white;
      }
    }

    .message {
      animation: fadeIn 0.5s ease forwards;
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
        animation: glow 3s ease-in-out infinite alternate;
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
        animation: glow 3s ease-in-out infinite alternate;
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
        animation: glow 2.5s ease-in-out infinite alternate;
    }
    button:hover {
        background-color: #3700B3;
    }
    </style>

    <!-- Скрипт автоскролла к последнему сообщению -->
    <script>
    const scrollToBottom = () => {
      const chat = document.getElementById('chat-history');
      if (chat) {
        chat.scrollTop = chat.scrollHeight;
      }
    }
    window.onload = scrollToBottom;
    </script>
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

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

def send_message():
    user_text = st.session_state.text_input.strip()
    if not user_text:
        return

    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.text_input = ""
    st.session_state.is_typing = True

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

    st.session_state.is_typing = False

st.text_input("Write your revelation:", key="text_input", on_change=send_message)

st.button("💬", on_click=send_message)

st.markdown("---")
st.subheader("📖 Chat history:")

# Контейнер для чата с id для автоскролла
st.markdown('<div id="chat-history" style="height:400px; overflow-y:auto;">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f'<div class="user-bubble message clearfix">{content}</div>', unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f'<div class="bot-bubble message clearfix">{content}</div>', unsafe_allow_html=True)

# Индикатор набора текста
if st.session_state.is_typing:
    st.markdown(
        '<div class="bot-bubble message clearfix typing-indicator">Bot is typing</div>',
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
