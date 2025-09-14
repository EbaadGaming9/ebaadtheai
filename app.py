import re
import streamlit as st
from groq import Groq

# ---------------------------
# Page config (favicon only)
# ---------------------------
st.set_page_config(
    page_title="Ebaad AI",
    page_icon="Logo.png",   # favicon in browser tab (use exact file name in your repo)
    layout="centered",
)

# ---------------------------
# System prompt (keeps the model 'in character')
# ---------------------------
SYSTEM_PROMPT = (
    "You are Ebaad, a helpful personal AI assistant. "
    "Always identify as 'Ebaad' when asked your name, and always say 'Ebaad developed me' "
    "or similar phrasing when asked who created you. Be friendly, concise, and helpful."
)

# ---------------------------
# Helper: canned identity replies (guaranteed, no API call)
# ---------------------------
def canned_identity_reply(text: str) -> str | None:
    t = text.lower().strip()

    # Who made / developed you
    if re.search(r"\bwho (made|created|developed) (you|this|the bot|the assistant)\b", t) \
       or re.search(r"\bwho (is )?your (creator|maker|developer)\b", t):
        return "Ebaad developed me."

    # Name / who are you
    if re.search(r"\bwhat('?s| is) your name\b", t) \
       or re.search(r"\bwho are you\b", t) \
       or re.search(r"\bwho am i talking to\b", t) \
       or re.search(r"\bwhat should i call you\b", t):
        return "My name is Ebaad."

    return None

# ---------------------------
# Initialize session state
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ---------------------------
# UI header
# ---------------------------
st.title("🤖 Ebaad - Your Personal AI")
st.write("Your personal AI assistant — ask me anything.")

# ---------------------------
# Groq client (load key from Streamlit Secrets)
# ---------------------------
# Make sure you set GROQ_API_KEY in Streamlit Cloud secrets (not in code)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------------------
# Show chat history (skip system messages)
# ---------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# ---------------------------
# Input & handling
# ---------------------------
if prompt := st.chat_input("Ask Ebaad anything..."):
    # Save and show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Check canned reply first (identity/name)
    canned = canned_identity_reply(prompt)
    if canned:
        st.session_state.messages.append({"role": "assistant", "content": canned})
        st.chat_message("assistant").markdown(canned)
    else:
        # Call model
        with st.chat_message("assistant"):
            try:
                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",  # supported model — update if Groq deprecates it
                    messages=st.session_state.messages,
                )
                reply = resp.choices[0].message.content
            except Exception as e:
                # Friendly error to users; detailed error in logs
                st.error("Sorry — Ebaad had trouble answering. Check the app logs (Manage app).")
                # also append a short assistant message so conversation stays consistent
                reply = "I'm having trouble accessing my model right now. Please try again later."

            # display & save reply
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------------------------
# Optional: small footer (non-invasive)
# ---------------------------
st.markdown("---")
st.caption("⚡ Developed by Ebaad")
