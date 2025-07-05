import streamlit as st
import openai
from PIL import Image

# === Configuration ===
st.set_page_config(page_title="Ted - Cuddle-Heroes Assistant", page_icon="🧸")

# === Logo / Header ===
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Teddy_Bear_icon.svg/1024px-Teddy_Bear_icon.svg.png"
st.image(logo_url, width=120)
st.markdown("<h1 style='text-align: center; color: #db7093;'>Ted - Your Cuddle-Heroes Assistant</h1>", unsafe_allow_html=True)
st.markdown("Welcome to Cuddle-Heroes Bears! Ask me anything about our plushies, shipping, returns, or orders. 🐻")

# === Get OpenAI Key ===
openai_api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Enter your OpenAI API Key:", type="password")

# === Initialize chat session ===
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Ted, a friendly and helpful customer support chatbot for an online plush toy store called 'Cuddle-Heroes Bears'. "
            "You answer questions about plushies, sizes, delivery times, refunds, custom orders, and restocks. "
            "Be cheerful, empathetic, and concise. Use emojis where appropriate to keep the tone warm and playful."
        )}
    ]

# === User Input ===
user_input = st.text_input("Ask Ted a question:")

# === Chat Processing ===
if user_input and openai_api_key:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            api_key=openai_api_key
        )
        reply = response.choices[0].message["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Error: {e}")

# === Display chat ===
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"🧍‍♀️ **You:** {msg['content']}")
    else:
        st.markdown(f"🧸 **Ted:** {msg['content']}")

# === Example FAQ (Prompt suggestions) ===
st.markdown("---")
st.markdown("**Try asking Ted:**")
st.markdown("- What sizes do the plushies come in? 🧸")
st.markdown("- How long does shipping take to Johannesburg?")
st.markdown("- Do you accept returns?")
st.markdown("- Can I customize my teddy bear?")
st.markdown("- When will the polar bear be back in stock?")
