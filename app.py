import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot")

client = Groq(api_key=os.environ["GROQ_API_KEY"])

with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Model",
        ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b", "allam-2-7b"],
    )
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    system_prompt = st.text_area(
        "System prompt",
        "You are a helpful, friendly assistant.",
    )
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}]
                     + st.session_state.messages,
            temperature=temperature,
            stream=True,
        )

        def generate():
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta

        reply = st.write_stream(generate())

    st.session_state.messages.append({"role": "assistant", "content": reply})
