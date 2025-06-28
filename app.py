import streamlit as st
import openai
import os
import json
from datetime import datetime, timedelta

st.set_page_config(page_title="Whisper Translator", layout="centered")

# 🔑 API key
openai.api_key = st.secrets["openai_api_key"]
client = openai.OpenAI(api_key=openai.api_key)

# 📁 История
HISTORY_FILE = "chat_history.json"
BOOK_FILE = "soul_book.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_book():
    if os.path.exists(BOOK_FILE):
        with open(BOOK_FILE, "r") as f:
            return json.load(f)
    return {}

def save_book(book):
    with open(BOOK_FILE, "w") as f:
        json.dump(book, f, ensure_ascii=False, indent=2)

# 🤖 Session
if "messages" not in st.session_state:
    st.session_state.messages = load_history()
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
if "soul_book" not in st.session_state:
    st.session_state.soul_book = load_book()

# 🌟 Стили
st.markdown("""
<style>
html, body, [class*="css"] {
    background: linear-gradient(to top, #4b0082 0%, black 90%) !important;
    color: white;
}
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.bubble-user {
    background-color: rgba(186, 85, 211, 0.25);
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    width: fit-content;
    max-width: 80%;
    animation: fadeIn 0.6s ease-in-out;
}
.bubble-bot {
    background-color: rgba(173, 216, 230, 0.25);
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
.typing-indicator {
    font-size: 20px;
    margin: 20px 0;
    text-align: center;
    animation: blink 1.5s infinite;
}
@keyframes blink {
    0% { opacity: 0.2; }
    50% { opacity: 1; }
    100% { opacity: 0.2; }
}
</style>
""", unsafe_allow_html=True)

# 📚 Название
st.title("Whisper Translator")
st.write("Today, you can share what your soul feels.")

# 📒 История
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        bubble_class = "bubble-user" if role == "user" else "bubble-bot"
        st.markdown(f'<div class="{bubble_class}">{content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 📅 Проверка начала недели
now = datetime.now()
week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
if week_start not in st.session_state.soul_book:
    if len(st.session_state.messages) >= 3:
        summary_prompt = """Summarize the essence of this week's conversation as a poetic, reflective chapter. Title it."""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a poetic soul narrator."},
                *st.session_state.messages[-10:],
                {"role": "user", "content": summary_prompt},
            ]
        )
        chapter = response.choices[0].message.content
        st.session_state.soul_book[week_start] = chapter
        save_book(st.session_state.soul_book)

# 📝 Поле ввода
form = st.form("chat_form", clear_on_submit=False)
text_input = form.text_input(
    "Write your revelation:",
    value=st.session_state.text_input,
    label_visibility="collapsed"
)
submit = form.form_submit_button("💬")

if submit and text_input.strip():
    user_message = text_input.strip()
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.text_input = ""
    save_history(st.session_state.messages)

    with st.spinner("The soul is whispering..."):
        placeholder = st.empty()
        placeholder.markdown('<div class="typing-indicator">🌜 Thinking...</div>', unsafe_allow_html=True)

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a poetic and wise soul guide. Respond kindly and ask thoughtful questions."},
                    *st.session_state.messages
                ]
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            save_history(st.session_state.messages)
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            placeholder.empty()

# 📕 Книга души
with st.expander("📖 Soul Book: Weekly Chapters"):
    for week, chapter in st.session_state.soul_book.items():
        st.markdown(f"### Week of {week}\n{chapter}")
