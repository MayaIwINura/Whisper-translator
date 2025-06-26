import streamlit as st
import openai

client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

st.title("Whisper Translator")
st.write("Today, you can share what your soul feels.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a poetic and kind soul guide. Respond with empathy, deep insight, or a spiritual question."}
    ]

text = st.text_area("Write your revelation:")

if st.button("Send"):
    if text.strip():
        st.session_state.messages.append({"role": "user", "content": text})

        with st.spinner("Listening to the soul..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                gpt_reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": gpt_reply})
                st.markdown(f"GPT whispers back:\n\n> {gpt_reply}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
