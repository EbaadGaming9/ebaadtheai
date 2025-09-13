import streamlit as st
from groq import Groq

# ✅ Load API key from Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 Ebaad - Your Personal AI")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Say something to Ebaad..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # AI response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ Supported Groq model
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
