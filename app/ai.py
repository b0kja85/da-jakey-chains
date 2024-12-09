import os
from groq import Groq
import streamlit as st

from dotenv import load_dotenv

# Initialize the Groq client
load_dotenv()
api_key = os.getenv("GROQ_API_KEY") # Add your API Key Here
client = Groq(api_key=api_key)

def chatbot():
    st.header("🤖 Meet J(AI)ms Charter", anchor=False)
    st.write("Engage with an AI chatbot for assistance and answers to all your questions about Data Analytics.")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Initial AI prompt
    if len(st.session_state["messages"]) == 0:
        st.session_state["messages"].append({
            "role": "assistant",
            "content": (
                "📊 Hey there! My name is 🤖 J(AI)ms Charter and I'm here to help with all your data analysis needs!\n\n"
                "I'm an AI assistant specializing in data analysis concepts, methods, and best practices 🧠\n\n"
                "I can explain statistical techniques, data visualization approaches, and analytical methodologies 💡\n\n"
                "My goal is to make data analysis concepts fun and useful for you 😊\n\n"
                "Is there something specific you'd like help with today? Maybe you have a question about a particular statistical method, "
                "or perhaps you're looking for advice on visualizing your data? \n\n"
                "🗣️ I'm all ears...or should I say, all code! Let me know what's on your mind, "
                "and we'll get started on exploring the world of data analysis together."
            )
        })

    # Chat container placeholder
    with st.container(height=500, border=False):
        chat_placeholder = st.empty()

    # Render chat messages
    def render_chat():
        with chat_placeholder.container():
            for message in st.session_state["messages"]:
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.markdown(message["content"])
                elif message["role"] == "assistant":
                    with st.chat_message("assistant"):
                        st.markdown(message["content"])

    # Render existing messages
    render_chat()

    # User input field
    user_input = st.text_input(
        label="",
        placeholder="Ask J(AI)ms anything! Type your message here...",
        key="user_input",
    )

    if user_input:
        # Append user message
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Generate AI response
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    messages=st.session_state["messages"],
                    model="llama3-8b-8192"
                )
                ai_reply = response.choices[0].message.content
                st.session_state["messages"].append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                fallback_message = f"⚠️ An error occurred: {e}"
                st.session_state["messages"].append({"role": "assistant", "content": fallback_message})

        # Render updated chat
        render_chat()