import streamlit as st
from datetime import datetime
import time
import uuid

# Must be the first Streamlit command
st.set_page_config(
    page_title="Game Master",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

from src.agents.bedrock_agent import BedrockAgent
from src.services.storage_service import StorageService
from src.services.image_service import ImageService
from src.config.prompts import LAUNCH_PROMPT
from src.services.character_service import CharacterService

class GameMasterUI:
    def __init__(self):
        self._initialize_session_state()
        self._setup_page()

    def _setup_page(self):
        st.title("Game Master")
        
    def _initialize_session_state(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'agent' not in st.session_state:
            st.session_state.agent = BedrockAgent()
        if 'storage' not in st.session_state:
            st.session_state.storage = StorageService()
        if 'image_service' not in st.session_state:
            st.session_state.image_service = ImageService()
        if 'character_service' not in st.session_state:
            st.session_state.character_service = CharacterService()
        if 'name' not in st.session_state:
            st.session_state.name = None
        if 'character_created' not in st.session_state:
            st.session_state.character_created = False
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'character_creation'
        if 'launch_prompt_sent' not in st.session_state:
            st.session_state.launch_prompt_sent = False

    def _display_character_creation_page(self):
        st.header("Create Your Character")
        
        # Player name input
        name_input = st.text_input("What is your name adventurer?", key="name_input")
        if name_input:
            st.session_state.name = name_input
            
        # Race and Class selection
        col1, col2 = st.columns(2)
        
        with col1:
            race = st.selectbox(
                "What is your race?",
                [
                    "Human",
                    "Elf",
                    "Dwarf",
                    "Halfling",
                    "Gnome",
                    "Half-Elf",
                    "Half-Orc",
                    "Dragonborn",
                    "Tiefling"
                ],
                key="race"
            )
            
        with col2:
            character_class = st.selectbox(
                "What is your class?",
                [
                    "Fighter",
                    "Wizard",
                    "Rogue",
                    "Cleric",
                    "Ranger",
                    "Paladin",
                    "Barbarian",
                    "Bard",
                    "Druid",
                    "Monk",
                    "Sorcerer",
                    "Warlock"
                ],
                key="class"
            )
        
        st.divider()  # Add a visual separator
        
        # Stats
        st.subheader("Ability Scores")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            intelligence = st.number_input("Intelligence", min_value=0, max_value=20, value=10, key="intelligence")
            strength = st.number_input("Strength", min_value=0, max_value=20, value=10, key="strength")
        
        with col2:
            dexterity = st.number_input("Dexterity", min_value=0, max_value=20, value=10, key="dexterity")
            constitution = st.number_input("Constitution", min_value=0, max_value=20, value=10, key="constitution")
        
        with col3:
            wisdom = st.number_input("Wisdom", min_value=0, max_value=20, value=10, key="wisdom")
            charisma = st.number_input("Charisma", min_value=0, max_value=20, value=10, key="charisma")

        specs = {
            'character_name': name_input,
            'race': race,
            'class': character_class,
            'Intelligence': intelligence,
            'Strength': strength,
            'Dexterity': dexterity,
            'Constitution': constitution,
            'Wisdom': wisdom,
            'Charisma': charisma
        }

        if st.button("Start Adventure", disabled=not name_input):
            character_id = str(uuid.uuid4())
            
            # Show saving message
            with st.spinner("Saving your character..."):
                success = self.save_character(character_id, specs)
            
            if success:
                st.success(f"Character saved successfully! Preparing your adventure...")
                st.session_state.character_created = True
                st.session_state.current_character = specs
                st.session_state.current_page = 'game'
                st.rerun()  # This will immediately switch to the game page
            else:
                st.error("Failed to save character. Please try again.")

    def _display_game_page(self):
        # Setup sidebar with character info first
        with st.sidebar:
            st.title(st.session_state.current_character['character_name'])
            st.write(f"**{st.session_state.current_character['race']} {st.session_state.current_character['class']}**")
            
            st.divider()
            
            for stat, value in st.session_state.current_character.items():
                if stat not in ['character_name', 'race', 'class']:
                    modifier = (value - 10) // 2
                    modifier_text = f"+{modifier}" if modifier >= 0 else str(modifier)
                    st.write(f"{stat}: {value} ({modifier_text})")
            
            st.button("Save Game", on_click=self.save_game)

        # Show loading state for game initialization
        if not st.session_state.launch_prompt_sent:
            st.markdown("## Preparing Your Adventure")
            with st.spinner("The Game Master is preparing your adventure..."):
                character = st.session_state.current_character
                launch_prompt = LAUNCH_PROMPT.format(
                    player_name=character['character_name'],
                    player_race=character['race'],
                    player_class=character['class']
                )
                
                response = st.session_state.agent.get_response(launch_prompt)
                if response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.launch_prompt_sent = True
                    st.rerun()
                return  # Don't show the rest of the UI while loading

        # Main game area (only shown after launch prompt is sent)
        self._display_chat_history()
        
        if prompt := st.chat_input("What would you like to ask?", max_chars=1000):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
        # Handle new messages
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            with st.spinner("Thinking..."):
                response = st.session_state.agent.get_response(prompt)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

    def run(self):
        if st.session_state.current_page == 'character_creation':
            self._display_character_creation_page()
        else:
            self._display_game_page()

    def _generate_and_display_image(self, text):
        """Generate and display an image based on the text"""
        with st.spinner("Generating image..."):
            image = st.session_state.image_service.generate_image(text)
            if image:
                st.image(
                    image,
                    use_container_width=True,
                    output_format="PNG",
                    clamp=True
                )

    def _display_message(self, message):
        """Display a single message and its image if it's from the assistant"""
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                # Create two equal columns for better layout
                left_col, right_col = st.columns(2)
                
                # Game Master's response in left column
                with left_col:
                    st.markdown(message["content"])
                
                # Generated image in right column
                with right_col:
                    self._generate_and_display_image(message["content"])
            else:
                # Player's messages use full width
                st.markdown(message["content"])

    def _display_chat_history(self):
        """Display all messages with their images"""
        for message in st.session_state.messages:
            self._display_message(message)

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

    def save_character(self, character_id, specs):
        """Save character to the database"""
        return st.session_state.character_service.save_character(character_id, specs)

def main():
    app = GameMasterUI()
    app.run()

if __name__ == "__main__":
    main() 