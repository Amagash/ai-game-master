import streamlit as st
from src.agents.bedrock_agent import BedrockAgent
from src.services.storage_service import StorageService

class GameMasterUI:
    def __init__(self):
        self._initialize_session_state()
        self._setup_page()
        
    def _initialize_session_state(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'agent' not in st.session_state:
            st.session_state.agent = BedrockAgent()
        if 'storage' not in st.session_state:
            st.session_state.storage = StorageService()
        if 'name' not in st.session_state:
            st.session_state.name = None
    
    def _setup_page(self):
        st.set_page_config(
            page_title="Game Master",
            page_icon="🎲",
            layout="wide",
            initial_sidebar_state="auto",
            menu_items=None
        )
        st.title("Game Master")
    
    def _handle_name_input(self):
        with st.form("name_form"):
            name_input = st.text_input("What is your name adventurer?")
            submit_button = st.form_submit_button("Start")
            if submit_button and name_input:
                st.session_state.name = name_input
                launch_prompt = f"""The player's name is {st.session_state.name}. Describe the surroundings of the player and create an atmosphere that the player can bounce off of."""
                response = st.session_state.agent.get_response(launch_prompt)
                if response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

    def _handle_chat(self):
        if prompt := st.chat_input("What would you like to ask?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = st.session_state.agent.get_response(prompt)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})

    def _display_chat_history(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    def _setup_sidebar(self):
        if st.session_state.name is not None:
            with st.sidebar:
                st.button("Save Game", on_click=self.save_game)
    
    def save_game(self):
        if not st.session_state.messages:
            st.warning("No conversation to save!")
            return
            
        success, result = st.session_state.storage.save_game_session(
            st.session_state.messages, 
            st.session_state.name
        )
        
        if success:
            st.success(f"Game saved successfully as {result}!")
        else:
            st.error(f"Error saving game: {result}")
    
    def run(self):
        if st.session_state.name is None:
            self._handle_name_input()
        else:
            self._handle_chat()
            
        self._display_chat_history()
        self._setup_sidebar()

def main():
    app = GameMasterUI()
    app.run()

if __name__ == "__main__":
    main() 