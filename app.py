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

client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

st.title("Whisper Translator")
st.write("Today, you can share what your soul feels.")

history = load_history()

if "messages" not in st.session_state:
    if history:
        st.session_state.messages = history
    else:
        st.session_state.messages = [
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

text = st.text_area("Write your revelation:")

if st.button("💬"):
    if text.strip():
        st.session_state.messages.append({"role": "user", "content": text})

        with st.spinner("Listening to the soul..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                )
                gpt_reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": gpt_reply})

                save_history(st.sess_
