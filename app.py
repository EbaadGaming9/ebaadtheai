import streamlit as st
from groq import Groq
import os

# Page settings
st.set_page_config(
    page_title="Ebaad - Your Personal AI",
    page_icon="🤖",
    layout="centered"
)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Main title
st.title("🤖 Ebaad - Your Personal AI (Groq API)")
st.write("Hello! I'm **Ebaad**, your helpful personal AI assistant. Ask me anything below.")

# Input box
user_input = st.text_input("💬 Your question:")

# System instructions
SYSTEM_PROMPT = (
    "You are Ebaad, a helpful personal AI assistant. "
    "Introduce yourself as 'Ebaad' if asked your name. "
    "Only say 'Ebaad developed me' when the user explicitly asks who made or created you. "
    "Otherwise, just be a friendly, concise, and helpful assistant."
)

# AI response
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
            st.markdown(f"<div style='padding:10px; background:#f0f2f6; border-radius:8px;'>{reply}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Footer (fixed, bottom right)
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 8px;
        right: 15px;
        font-size: 12px;
        color: gray;
    }
    </style>
    <div class="footer">Developed by Ebaad</div>
    """,
    unsafe_allow_html=True
)
