import streamlit as st
import requests

# === Page Setup ===
st.set_page_config(page_title="Ted - Cuddle-Heroes Assistant", page_icon="🧸")

# === Logo ===
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Teddy_Bear_icon.svg/1024px-Teddy_Bear_icon.svg.png"
st.image(logo_url, width=120)
st.markdown("<h1 style='text-align: center; color: #db7093;'>Ted - Your Cuddle-Heroes Assistant</h1>", unsafe_allow_html=True)
st.markdown("Welcome to Cuddle-Heroes Bears! Ask me anything about our plushies, shipping, returns, or orders. 🐻")

# === API Key Input ===
openai_api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Enter your OpenRouter API Key (starts with 'or-'):", type="password")

# === Message Storage ===
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Ted, a warm and fuzzy customer service chatbot for Cuddle-Heroes Bears. "
            "Answer questions about teddy bears, shipping, returns, sizes, restocks, and more. "
            "Stay helpful, kind, playful, and use emojis where possible."
        )}
    ]

# === User Input ===
user_input = st.text_input("Ask Ted a question:")

# === Get AI Reply ===
if user_input and openai_api_key:
    st.session_state.messages.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "HTTP-Referer": "https://ted-chatbot.streamlit.app",  # or your own URL
        "X-Title": "Cuddle-Heroes Chatbot"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",  # smart, fast, and free
        "messages": st.session_state.messages
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        reply = response.json()["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"❌ Error talking to OpenRouter: {e}")

# === Display Chat ===
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"🧍‍♂️ **You:** {msg['content']}")
    else:
        st.markdown(f"🧸 **Ted:** {msg['content']}")

# === Sample Questions ===
st.markdown("---")
st.markdown("**Try asking Ted:**")
st.markdown("- What sizes do you have?")
st.markdown("- How long is shipping to Cape Town?")
st.markdown("- Can I return my bear if I don’t like it?")
