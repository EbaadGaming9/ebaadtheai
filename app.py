import streamlit as st
from groq import Groq
import os

# Page config
st.set_page_config(
    page_title="Ebaad - Your Personal AI",
    page_icon="Logo.png",  # Tab icon
    layout="centered"
)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Title
st.title("🤖 Ebaad - Your Personal AI (Groq API)")

# System instructions
SYSTEM_PROMPT = (
    "You are Ebaad, a helpful personal AI assistant. "
    "If someone asks 'who made you', 'who developed you', or similar, "
    "you must answer only: 'I was developed by Ebaad'. "
    "Otherwise, act as a friendly, smart, and concise assistant named Ebaad."
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system
    if msg["role"] == "user":
        with st.chat_message("user"):  # 👈 no avatar
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="Logo.png"):
            st.markdown(msg["content"])

# Input box
if user_input := st.chat_input("Type your message..."):
    # Show user
    with st.chat_message("user"):  # 👈 no avatar
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # ✅ supported
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content

            # Show assistant
            with st.chat_message("assistant", avatar="Logo.png"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Footer credit
st.markdown("<p style='text-align: right; color: gray; font-size: 12px;'>Developed by Ebaad</p>", unsafe_allow_html=True)
