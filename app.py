import boto3
import streamlit as st

from agent import BedrockAgent
from utils import save_game

# Set page config without theme parameter
st.set_page_config(page_title="Game Master", page_icon="🎲", layout="wide", initial_sidebar_state="auto", menu_items=None)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize agent in session state
if 'agent' not in st.session_state:
    st.session_state.agent = BedrockAgent()

# Initialize S3 client in session state
if 's3_client' not in st.session_state:
    st.session_state.s3_client = boto3.client('s3')

# App title
st.title("Game Master")

# Initialize name in session state if not present
if 'name' not in st.session_state:
    st.session_state.name = None

# Name input form
if st.session_state.name is None:
    with st.form("name_form"):
        name_input = st.text_input("What is your name adventurer?")
        submit_button = st.form_submit_button("Start")
        if submit_button and name_input:
            st.session_state.name = name_input
            # Hidden system prompt for the agent
            launch_prompt = f"""The player's name is {st.session_state.name}. Describe the surroundings of the player and create an atmosphere that the player can bounce off of."""
            
            # Get response from agent
            response = st.session_state.agent.get_response(launch_prompt)
            
            # Only add the agent's response to visible chat history
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# Chat input (moved outside the name check block)
if prompt := st.chat_input("What would you like to ask?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = st.session_state.agent.get_response(prompt)
    if response:
        st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history (moved outside the name check block)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Add save button to the sidebar
if st.session_state.name is not None:
    with st.sidebar:
        st.button("Save Game", on_click=save_game) 