import streamlit as st
import ollama
import base64

# Set page config
st.set_page_config(page_title="Mental Health Chatbot", layout="wide")

# Background image setup
def get_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("background.png")

# CSS styling for background and buttons
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    button[kind="primary"], button {{
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-size: 16px !important;
        color: white !important;
        border: none !important;
        cursor: pointer !important;
        background: linear-gradient(270deg, #ff0000, #ffa500, #ffff00, #00ff00, #0000ff, #4b0082, #ee82ee);
        background-size: 1400% 1400%;
        animation: rainbow 10s ease infinite;
        transition: box-shadow 0.3s ease !important;
        box-shadow: 0 0 8px white;
    }}

    button[kind="primary"]:hover, button:hover {{
        box-shadow: 0 0 20px white;
    }}

    @keyframes rainbow {{
        0%{{background-position:0% 50%;}}
        50%{{background-position:100% 50%;}}
        100%{{background-position:0% 50%;}}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Custom title
st.markdown(
    """
    <h1 style='
        color: #f60606;
        text-align: center;
        font-family: "Arial", sans-serif;
        text-shadow: 3px 3px 2px #0000;
        padding: 20px 0;
    '>TAKE CARE OF YOUR HEALTH</h1>
    """,
    unsafe_allow_html=True
)

# Custom label
st.markdown(
    """
    <label style='
        color: #9bac0e;
        font-size: 20px;
        font-weight: bold;
    '>How can I help you today?</label>
    """,
    unsafe_allow_html=True
)

# Session state to keep chat history
st.session_state.setdefault('conversation_history', [])

# Functions for generating responses
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    response = ollama.chat(model="llama3.2", messages=st.session_state['conversation_history'])
    ai_response = response['message']['content']
    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed"
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Display conversation history with styled output
for msg in st.session_state['conversation_history']:
    if msg['role'] == "user":
        st.markdown(
            f"<div style='color: #0055ff; font-weight: bold;'>You: {msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='color: pink;'>AI: {msg['content']}</div>",
            unsafe_allow_html=True
        )

# Input box
user_message = st.text_input(label="", key="user_input")

if user_message:
    with st.spinner("Thinking....."):
        ai_response = generate_response(user_message)
        st.markdown(
            f"<div style='color: black;'>AI: {ai_response}</div>",
            unsafe_allow_html=True
        )

# Buttons for affirmation and meditation
col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"<div style='color: black;'>*Affirmation:* {affirmation}</div>", unsafe_allow_html=True)

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"<div style='color: black;'>*Guided Meditation:* {meditation_guide}</div>", unsafe_allow_html=True)
