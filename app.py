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
      background: black;
      background: linear-gradient(to top, #4b0082 0%, black 70%);
      color: white;
    }

    .main {
      padding: 1rem;
    }

    @keyframes fadeIn {
      from {opacity: 0; transform: translateY(10px);}
      to {opacity: 1; transform: translateY(0);}
    }

    @keyframes pulseButton {
      0%, 100% { box-shadow: 0 0 6px #8a2be2; }
      50% { box-shadow: 0 0 15px #8a2be2aa; }
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

    .user-bubble {
        background: linear-gradient(135deg, rgba(147,112,219,0.2), rgba(186,85,211,0.2));
        border-radius: 15px 15px 15px 0px;
        padding: 12px 15px;
        max-width: 70%;
        margin: 6px 0;
        color: white;
        float: left;
        clear: both;
        animation: fadeIn 0.5s ease forwards;
    }

    .bot-bubble {
        background: linear-gradient(135deg, rgba(144,238,144,0.2), rgba(60,179,113,0.2));
        border-radius: 15px 15px 0px 15px;
        padding: 12px 15px;
        max-width: 70%;
        margin: 6px 0;
        color: white;
        float: right;
        clear: both;
        animation: fadeIn 0.5s ease forwards;
    }

    .typing-indicator::after {
      content: '...';
      animation: dots 1.5s steps(5, end) infinite;
      font-weight: bold;
      margin-left: 4px;
    }

    button {
        cursor: pointer;
        font-size: 20px;
        padding: 6px 12px;
        border-radius: 12px;
        border: none;
        background-color: #8a2be2;
        color: white;
        animation: pulseButton 3s ease-in-out infinite;
    }
    button:hover {
        background-color: #5d1ba3;
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

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

def send_message():
    user_text = st.session_state.text_input.strip()
    if not user_text:
        return

    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.text_input = ""
    st.session_state.is_typing = True

    save_history(st.session_state.messages)

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

# Текстовое поле и кнопка отправки
st.text_input("Write your revelation:", key="text_input", on_change=send_message)
st.button("💬", on_click=send_message)

st.markdown("---")

# Отображение сообщений
for msg in st.session_state.messages[1:]:  # пропускаем system
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

# Индикатор "печатает"
if st.session_state.is_typing:
    st.markdown('<div class="bot-bubble typing-indicator">Bot is typing</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
