import streamlit as st
from groq import Groq

# ---------------------------
# Page Config (sets tab title + favicon)
# ---------------------------
st.set_page_config(
    page_title="Ebaad AI",
    page_icon="Logo.png",   # this shows in the browser tab
    layout="centered"
)

# ---------------------------
# Custom CSS to hide Streamlit branding + add footer
# ---------------------------
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #111;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown('<div class="footer">⚡ Developed by Ebaad</div>', unsafe_allow_html=True)

# ---------------------------
# Title
# ---------------------------
st.title("🤖 Welcome to Ebaad AI")
st.write("Your personal AI assistant, developed by Ebaad ✨")

# ---------------------------
# Groq API Setup
# ---------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------------------
# Chatbot UI
# ---------------------------
user_input = st.text_input("💬 Ask me anything:")

if user_input:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Ebaad AI, a helpful assistant developed by Ebaad."},
                {"role": "user", "content": user_input},
            ],
        )
        reply = response.choices[0].message.content
        st.success(reply)
