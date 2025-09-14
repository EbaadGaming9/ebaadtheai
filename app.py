import streamlit as st
from groq import Groq
import os

# Page config
st.set_page_config(
    page_title="Ebaad - Your Personal AI",
    page_icon="🤖",
    layout="centered"
)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Title
st.title("🤖 Ebaad - Your Personal AI (Groq API)")

# System instructions
SYSTEM_PROMPT = (
    "You are Ebaad, a helpful personal AI assistant. "
    "Introduce yourself as 'Ebaad' if asked your name. "
    "Only say 'Ebaad developed me' when the user explicitly asks who made or created you. "
    "Otherwise, just be a friendly, concise, and helpful assistant."
)

# CSS for bubbles
st.markdown(
    """
    <style>
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 15px;
    }
    .user-bubble {
        background-color: #DCF8C6;
        margin-left: auto;
        text-align: right;
    }
    .assistant-bubble {
        background-color: #F1F0F0;
        margin-right: auto;
        text-align: left;
    }
    .footer {
        position: fixed;
        bottom: 8px;
        right: 15px;
        font-size: 12px;
        color: gray;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system prompt
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(f"<div class='chat-bubble user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"<div class='chat-bubble assistant-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

# Chat input
if user_input := st.chat_input("Type your message..."):
    # Show user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(f"<div class='chat-bubble user-bubble'>{user_input}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # ✅ supported model
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content

            # Show assistant reply
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"<div class='chat-bubble assistant-bubble'>{reply}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Footer
st.markdown("<div class='footer'>Developed by Ebaad</div>", unsafe_allow_html=True)
