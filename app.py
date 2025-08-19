# app.py
import streamlit as st
import uuid
import os
from chatbot import create_chatbot, get_response

# Set page title and configuration
st.set_page_config(
    page_title="OpenAI Chatbot",
    page_icon="🤖"
)

# Create a title for the app
st.title("🤖 AI Chatbot with Gemini-2.5-flash")

# Check for API key
if not os.getenv("OPENAI_API_KEY"):
    st.warning("⚠️ OpenAI API key not found. Set OPENAI_API_KEY in .env file.")

# Sidebar information
st.sidebar.header("About This Chatbot")
st.sidebar.markdown("""
This chatbot uses Gemini-2.5-flash model to answer AI-related questions.
It is configured to:
- Respond only to AI-related topics
- Provide concise, helpful answers
- Avoid asking questions
""")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
# Initialize chatbot
if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = create_chatbot()
    except Exception as e:
        st.error(f"Error initializing chatbot: {str(e)}")
        st.session_state.chatbot = None

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if user_input := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.chatbot:
                # Get response from the chatbot with the current messages
                response = get_response(
                    st.session_state.chatbot,
                    user_input,
                    st.session_state.messages
                )
                st.write(response)
            else:
                response = "Chatbot initialization failed. Please check your API key."
                st.error(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})