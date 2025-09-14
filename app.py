import re
import streamlit as st
from groq import Groq

# Load Groq key from Streamlit Secrets (do NOT hardcode if publishing)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# System prompt (defines Ebaad's identity, tone, and behavior)
SYSTEM_PROMPT = (
    "You are Ebaad, a helpful personal AI assistant created and owned by the user named Ebaad. "
    "Always identify as 'Ebaad' when asked your name, and always say 'Ebaad developed me' "
    "or similar phrasing when asked who created you. Be friendly, concise, and helpful."
)

st.set_page_config(page_title="Ebaad", page_icon="🤖")
st.title("🤖 Ebaad - Your Personal AI")

# Initialize chat history with the system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Helper: match user questions that should get canned answers
def check_canned_reply(user_text: str):
    text = user_text.lower().strip()

    # Patterns for "who made you" / "who developed you"
    made_patterns = [
        r"\bwho (made|created|developed) (you|this|the bot|the assistant)\b",
        r"\bwho (is )?your (creator|maker|developer)\b"
    ]
    for p in made_patterns:
        if re.search(p, text):
            return "Ebaad developed me."

    # Patterns for "what is your name" / "who are you"
    name_patterns = [
        r"\bwhat'?s your name\b",
        r"\bwhat is your name\b",
        r"\bwho are you\b",
        r"\bwho am i talking to\b",
        r"\bwhat should i call you\b"
    ]
    for p in name_patterns:
        if re.search(p, text):
            return "My name is Ebaad."

    # Add other canned replies here as needed:
    # e.g., r"\bwhere are you from\b" -> "I was created by Ebaad."
    return None

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])
    # ignore system messages in the UI

# Input
if prompt := st.chat_input("Ask Ebaad anything..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Check for canned reply first (guarantees consistent identity)
    canned = check_canned_reply(prompt)
    if canned:
        # Return canned reply immediately (no API call)
        st.session_state.messages.append({"role": "assistant", "content": canned})
        st.chat_message("assistant").markdown(canned)
    else:
        # Otherwise, call the model with full conversation
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # or another supported model
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

        # Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": reply})
