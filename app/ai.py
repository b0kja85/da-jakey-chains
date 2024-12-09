import os
from groq import Groq
import streamlit as st

# Initialize the Groq client
os.environ["GROQ_API_KEY"] = "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"
client = Groq()

def chatbot():
    """Render the chatbot interface in Streamlit with a small, sticky input box."""
    # Inject custom CSS for compact and chat-like design
    st.markdown(
        """
        <style>
        /* General Chat Styling */
        .stChatMessage {
            margin-bottom: 10px;
        }
        .stChatMessage div {
            font-size: 14px;
        }

        /* Sticky input box */
        div.stTextInput {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 800px;
            z-index: 10;
            opacity: 0.8;
        }

        div.stTextInput input {
            height: 30px;
            border: none;
            font-size: 14px;
            outline: none;
            padding: 5px 10px;
            border-radius: 15px;
            width: 100%;
            background-color: #f7f7f7;
        }

        div.stTextInput input:focus {
            border: none;
            outline: none;
        }

        /* Padding to prevent overlap with sticky input box */
        .stApp {
            padding-bottom: 70px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.header("🤖 Ask AI", anchor=False)
    st.write("Interact with AI to get assistance or ask questions about your data or app functionality.")

    # Initialize session state to store chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display the chat history
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # Handle user input (stickied at bottom, compact style)
    if "new_input" not in st.session_state:
        st.session_state["new_input"] = ""

    user_input = st.text_input(
        "",  # Remove label
        placeholder="Type your message here...",
        key="new_input",  # Use a separate key
    )
    if user_input:
        # Save user input in the session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response from Groq AI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        messages=st.session_state["messages"],  # Send conversation history
                        model="llama3-8b-8192",  # Specify the model
                    )
                    ai_reply = response.choices[0].message.content
                    st.markdown(ai_reply)
                    # Save assistant's response in session state
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

