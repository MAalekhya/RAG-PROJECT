import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #ffffff;
        border: 1px solid #4a4a4a;
    }
    .chat-bubble {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #007bff;
        background-color: #1e1e1e;
    }
    .user-bubble {
        border-left: 5px solid #2ecc71;
    }
    .ai-bubble {
        border-left: 5px solid #3498db;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Gemini AI Assistant")
st.markdown("---")

# API Configuration
API_URL = "http://localhost:8000/chat"

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is on your mind?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Thinking...*")
        
        try:
            response = requests.post(API_URL, json={"prompt": prompt})
            if response.status_code == 200:
                full_response = response.json()["response"]
                message_placeholder.markdown(full_response)
                # Add AI response to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                error_msg = f"Error: {response.text}"
                message_placeholder.error(error_msg)
        except Exception as e:
            message_placeholder.error(f"Failed to connect to backend: {e}")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("This is a Gemini-powered chat application built with FastAPI and Streamlit.")
    st.info("The backend handles real-time tool calling (like getting the current time) and uses the modern Google Generative AI SDK.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
