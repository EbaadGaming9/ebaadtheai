import streamlit as st
from groq import Groq
import os

# Set page config
st.set_page_config(
    page_title="Ebaad - Your Personal AI",
    page_icon="🤖",
    layout="centered"
)

# Initialize Groq client with your API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Title
st.title("🤖 Ebaad - Your Personal AI (Groq API)")

# Description
st.write("Hello! I'm **Ebaad**, your helpful personal AI assistant. Ask me anything!")

# User input
user_input = st.text_input("💬 Ask Ebaad something:")

# System instructions
SYSTEM_PROMPT = (
    "You are Ebaad, a helpful personal AI assistant. "
    "Introduce yourself as 'Ebaad' if asked your name. "
    "Only say 'Ebaad developed me' when the user explicitly asks who made or created you. "
    "Otherwise, just be a friendly, concise, and helpful assistant."
)

# Response handling
if user_input:
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # ✅ Supported Groq model
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
            )

            reply = response.choices[0].message.content
            st.success(reply)

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Footer credit
st.markdown(
    """
    <div style="position: fixed; bottom: 10px; right: 10px; font-size: 12px; color: gray;">
        Developed by Ebaad
    </div>
    """,
    unsafe_allow_html=True
)
