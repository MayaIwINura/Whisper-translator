import streamlit as st
import openai

# Используем новый клиент OpenAI
client = openai.OpenAI(api_key=st.secrets["openai_api_key"])

st.title("Whisper Translator")
st.write("Today, you can share what your soul feels.")

text = st.text_area("Write your revelation:")

if st.button("Send"):
    st.write("Thank you. I have heard your inner voice.")

    if text.strip():
        with st.spinner("Listening to the soul..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a poetic and kind soul guide. Respond with empathy, deep insight, or a spiritual question."
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ]
                )
                gpt_reply = response.choices[0].message.content
                st.markdown(f"GPT whispers back:\n\n> {gpt_reply}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
