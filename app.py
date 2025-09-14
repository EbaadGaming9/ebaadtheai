import streamlit as st
from groq import Groq
import os

# ✅ Set up the page (title, favicon, layout)
st.set_page_config(
    page_title="Ebaad AI",
    page_icon="🤖",
    layout="centered"
)

# ✅ Add custom CSS for bottom-right signature
st.markdown(
    """
    <style>
    .developed-by {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 14px;
        color: #888;
        font-family: Arial, sans-serif;
    }
    </style>
    <div class="developed-by">Developed by Ebaad</div>
    """,
    unsafe_allow_html=True
)

# ✅ Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("🚨 Missing API key! Please set GROQ_API_KEY in your environment variables.")
else:
    client = Groq(api_key=api_key)

# ✅ System prompt
SYSTEM_PROMPT = (
    "You are Ebaad, a helpful personal AI assistant. "
    "Introduce yourself as 'Ebaad' if asked your name. "
    "Only say 'Ebaad developed me' when the user explicitly asks who made or created you. "
    "Otherwise, just be a friendly, concise, and helpful assistant."
)

# ✅ Title
st.title("🤖 Ebaad - Your Personal AI (Groq API)")

# ✅ Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ✅ Show chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Groq API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.2-70b-text-preview",  # ✅ Stable supported model
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *st.session_state["messages"],
                    ],
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ Error: {e}"

        st.markdown(reply)
        st.session_state["messages"].append({"role": "assistant", "content": reply})

