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
st.write("Chat with your assistant below:")

# System instructions
SYSTEM_PROMPT = (
    "You are Ebaad, a helpful personal AI assistant. "
    "Introduce yourself as 'Ebaad' if asked your name. "
    "Only say 'Ebaad developed me' when the user explicitly asks who made or created you. "
    "Otherwise, just be a friendly, concise, and helpful assistant."
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Show previous messages (chat history)
for msg in st.session_state.messages[1:]:  # skip system prompt
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"🤖 **Ebaad:** {msg['content']}")

# Chat input box
user_input = st.chat_input("Type your message...")

# Handle new input
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"🧑 **You:** {user_input}")

    # Get AI response
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # ✅ Supported Groq model
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content

            # Add assistant reply
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.markdown(f"🤖 **Ebaad:** {reply}")

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
