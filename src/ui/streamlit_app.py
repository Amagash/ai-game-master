# Standard library imports
from datetime import datetime
import uuid
import re
import time
import random
import requests
import json

# AWS SDK + Retry imports
from botocore.exceptions import EventStreamError
from tenacity import retry, stop_after_attempt, wait_exponential

# Third-party imports
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Game Master",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Local application imports
from src.agents.bedrock_agent import BedrockAgent
from src.services.storage_service import StorageService
from src.services.image_service import ImageService
from src.services.character_service import CharacterService
from src.config.prompts import LAUNCH_PROMPT, SUGGESTION_PROMPT


class GameMasterUI:
    """
    Main UI class for the Game Master application.
    
    This class handles all UI components, including character creation,
    game display, chat interactions, and image generation.
    """
    
    def __init__(self):
        """Initialize the GameMasterUI and set up session state variables."""
        self._initialize_session_state()
        self.rate_limiter = RateLimiter(2.0)  # 2 requests per second

    def _initialize_session_state(self):
        """
        Initialize all session state variables needed for the application.
        
        This includes messages, services, character information, and UI state.
        """
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
        if 'suggestions' not in st.session_state:
            st.session_state.suggestions = []
        if 'last_message_had_suggestions' not in st.session_state:
            st.session_state.last_message_had_suggestions = False
        if 'generated_images' not in st.session_state:
            st.session_state.generated_images = {}  # Store images by message index

    def _display_character_creation_page(self):
        """
        Display the character creation interface.
        
        Includes fields for character name, race, class, gender, and ability scores.
        """
        st.header("Create Your Character")
        
        # Player name input
        name_input = st.text_input("What is your name adventurer?", key="name_input")
        if name_input:
            st.session_state.name = name_input
            
        # Race, Class, and Gender selection
        col1, col2, col3 = st.columns(3)
        
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
            
        with col3:
            gender = st.selectbox(
                "What is your gender?",
                [
                    "Male",
                    "Female",
                    "Non-binary",
                    "Other"
                ],
                key="gender"
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

        # Collect all character specifications
        specs = {
            'character_name': name_input,
            'race': race,
            'class': character_class,
            'gender': gender,
            'Intelligence': intelligence,
            'Strength': strength,
            'Dexterity': dexterity,
            'Constitution': constitution,
            'Wisdom': wisdom,
            'Charisma': charisma
        }

        # Start adventure button
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
                
                # Use a short delay to ensure the success message is seen
                time.sleep(1)
                
                # Force a complete page refresh
                st.rerun()
            else:
                st.error("Failed to save character. Please try again.")

    def _display_game_page(self):
        """
        Display the main game interface.
        
        Includes the character sidebar, chat history, suggestion buttons,
        and text input for player actions.
        """
        # Setup sidebar with character info first
        with st.sidebar:
            st.title(st.session_state.current_character['character_name'])
            st.write(f"**{st.session_state.current_character['race']} {st.session_state.current_character['class']}**")
            st.write(f"**Gender:** {st.session_state.current_character['gender']}")
            
            st.divider()
            
            # Display character stats with modifiers
            for stat, value in st.session_state.current_character.items():
                if stat not in ['character_name', 'race', 'class', 'gender']:
                    modifier = (value - 10) // 2
                    modifier_text = f"+{modifier}" if modifier >= 0 else str(modifier)
                    st.write(f"{stat}: {value} ({modifier_text})")
            
            st.button("Save Game", on_click=self.save_game)

        # Main game area
        self._display_chat_history()
        
        # Debug information about suggestions
        print(f"Current suggestions in session state: {st.session_state.suggestions}")
        
        # Display suggestion buttons if available - make them more prominent
        if st.session_state.suggestions and len(st.session_state.suggestions) > 0:
            
            # Create a container with a light background for better visibility
            suggestion_container = st.container()
            with suggestion_container:
                cols = st.columns(min(3, len(st.session_state.suggestions)))
                for i, suggestion in enumerate(st.session_state.suggestions[:3]):  # Limit to 3 suggestions
                    with cols[i]:
                        if st.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
                            self._handle_user_input(suggestion)
            
            st.markdown("---")  # Add a separator
        else:
            # If no suggestions are available, show a message and default suggestions
            st.warning("No specific suggestions available. Here are some general actions you can take:")
            
            default_suggestions = [
                "Explore the area",
                "Talk to someone nearby",
                "Check your inventory"
            ]
            
            suggestion_container = st.container()
            with suggestion_container:
                cols = st.columns(3)
                for i, suggestion in enumerate(default_suggestions):
                    with cols[i]:
                        if st.button(suggestion, key=f"default_suggestion_{i}", use_container_width=True):
                            self._handle_user_input(suggestion)
            
            st.markdown("---")  # Add a separator
        
        # Regular text input
        if prompt := st.chat_input("Or type what you would like to do...", max_chars=1000):
            self._handle_user_input(prompt)

    # def _handle_user_input(self, prompt):
    #     """
    #     Process user input and get AI response.
        
    #     Args:
    #         prompt (str): The user's input text
            
    #     This method adds the user message to chat history, gets an AI response,
    #     generates an image for the response, and updates suggestions.
    #     """
    #     # Add user message to chat history
    #     st.session_state.messages.append({"role": "user", "content": prompt})
        
    #     # Clear suggestions after user input
    #     st.session_state.suggestions = []
        
    #     # Get AI response
    #     with st.spinner("Thinking..."):
    #         if prompt == 'Talk to someone nearby':
    #             print('ici')
    #         response = st.session_state.agent.get_response(prompt)
    #         print(f"AI response: {response}")
            
    #     if response:
    #         # Add the new message to the chat history
    #         message_index = len(st.session_state.messages)
    #         st.session_state.messages.append({"role": "assistant", "content": response})
            
    #         # Generate image for the new message only
    #         with st.spinner("Generating image for the new response..."):
    #             image = st.session_state.image_service.generate_image(response)
    #             if image:
    #                 # Store the generated image in session state
    #                 st.session_state.generated_images[message_index] = image
            
    #         # Always generate new suggestions after AI response
    #         self._generate_suggestions(response)
            
    #         st.rerun()

    def _generate_suggestions(self, context):
        """
        Generate action suggestions based on the current context.
        
        Args:
            context (str): The current game context (usually the last AI response)
            
        This method uses the AI to generate contextually relevant action suggestions
        for the player to choose from.
        """
        try:
            character = st.session_state.current_character
            suggestion_prompt = SUGGESTION_PROMPT.format(
                player_name=character['character_name'],
                player_race=character['race'],
                player_class=character['class'],
                player_gender=character['gender'],
                context=context
            )
            
            print(f"Generating suggestions based on context: {context[:100]}...")
            
            with st.spinner("Generating suggestions..."):
                suggestions_text = st.session_state.agent.get_response(suggestion_prompt)
                print(f"Raw suggestions response: {suggestions_text}")
                
                # Extract suggestions using regex
                suggestions = re.findall(r'\d+\.\s+(.*?)(?=\n\d+\.|\Z)', suggestions_text, re.DOTALL)
                
                # Clean up suggestions
                suggestions = [s.strip() for s in suggestions if s.strip()]
                print(f"Extracted suggestions: {suggestions}")
                
                if suggestions:
                    st.session_state.suggestions = suggestions[:3]  # Limit to 3 suggestions
                else:
                    # Fallback if no suggestions were extracted
                    st.session_state.suggestions = [
                        "Explore the area",
                        "Talk to someone nearby",
                        "Check your inventory"
                    ]
                    print("Using fallback suggestions")
            
            print(f"Final suggestions set: {st.session_state.suggestions}")
        except Exception as e:
            error_msg = f"Error generating suggestions: {str(e)}"
            print(error_msg)
            # Provide default suggestions if generation fails
            st.session_state.suggestions = [
                "Explore the area",
                "Talk to someone nearby",
                "Check your inventory"
            ]
            print("Using default suggestions due to error")

    def run(self):
        """
        Main method to run the application.
        
        Handles page routing between character creation and game pages,
        and manages the initial game setup.
        """
        # Use a placeholder for the entire UI to allow complete clearing
        main_container = st.empty()
        
        if st.session_state.current_page == 'character_creation':
            # Display character creation page
            with main_container.container():
                st.title("Game Master")  # Display title once at the top
                self._display_character_creation_page()
        else:
            # Game page - first clear any previous content completely
            main_container.empty()
            
            # Create a new container for game content
            game_container = st.container()
            
            with game_container:
                if not st.session_state.launch_prompt_sent:
                    # Show loading state
                    st.title("Game Master")  # Display title once
                    st.markdown("## Preparing Your Adventure")
                    with st.spinner("The Game Master is preparing your adventure..."):
                        character = st.session_state.current_character
                        
                        # Set character info in the image service for consistent image generation
                        st.session_state.image_service.set_character_info(character)
                        
                        launch_prompt = LAUNCH_PROMPT.format(
                            player_name=character['character_name'],
                            player_race=character['race'],
                            player_class=character['class'],
                            player_gender=character['gender']
                        )
                        
                        response = st.session_state.agent.get_response(launch_prompt)
                        if response:
                            # Add the initial message
                            message_index = len(st.session_state.messages)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            
                            # Generate image for the initial message
                            with st.spinner("Generating your first adventure image..."):
                                image = st.session_state.image_service.generate_image(response)
                                if image:
                                    # Store the generated image
                                    st.session_state.generated_images[message_index] = image
                            
                            st.session_state.launch_prompt_sent = True
                            
                            # Generate initial suggestions based on the first response
                            self._generate_suggestions(response)
                            
                            st.rerun()
                else:
                    # Game is ready, display game page
                    st.title("Game Master")  # Display title once
                    self._display_game_page()

    def _generate_and_display_image(self, text, message_index):
        """
        Generate and display an image based on the text.
        
        Args:
            text (str): The text to generate an image from
            message_index (int): The index of the message in the chat history
            
        This method checks if an image already exists for the message,
        and only generates a new one if needed.
        """
        # Check if we already have this image generated
        if message_index in st.session_state.generated_images:
            # Use the stored image
            image = st.session_state.generated_images[message_index]
            st.image(
                image,
                use_container_width=True,
                output_format="PNG",
                clamp=True
            )
        else:
            # Generate a new image if we don't have it yet
            with st.spinner("Generating image..."):
                image = st.session_state.image_service.generate_image(text)
                if image:
                    # Store the image for future use
                    st.session_state.generated_images[message_index] = image
                    st.image(
                        image,
                        use_container_width=True,
                        output_format="PNG",
                        clamp=True
                    )

    def _display_message(self, message, index):
        """
        Display a single message and its image if it's from the assistant.
        
        Args:
            message (dict): The message to display
            index (int): The index of the message in the chat history
        """
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                # Create two equal columns for better layout
                left_col, right_col = st.columns(2)
                
                # Game Master's response in left column
                with left_col:
                    st.markdown(message["content"])
                
                # Generated image in right column
                with right_col:
                    self._generate_and_display_image(message["content"], index)
            else:
                # Player's messages use full width
                st.markdown(message["content"])

    def _display_chat_history(self):
        """
        Display all messages in the chat history with their images.
        """
        for i, message in enumerate(st.session_state.messages):
            self._display_message(message, i)

    def save_game(self):
        """
        Save the current game session to a PDF file in S3.
        
        Displays success or error messages to the user.
        """
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
        """
        Save character to the database.
        
        Args:
            character_id (str): The unique ID for the character
            specs (dict): The character specifications
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        return st.session_state.character_service.save_character(character_id, specs)

    @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=4, max=10),
            reraise=True
        )
    def _get_ai_response_with_retry(self, prompt: str) -> str:
        """
        Get AI response with exponential backoff retry mechanism.
        
        Args:
            prompt (str): The user input prompt
            
        Returns:
            str: The AI response
            
        Raises:
            EventStreamError: If all retry attempts fail
        """
        try:
            # Add jitter to prevent thundering herd
            jitter = random.uniform(0.1, 0.5)
            time.sleep(jitter)
            
            # Wait if rate limit requires
            wait_time = self.rate_limiter.acquire()
            if wait_time > 0:
                time.sleep(wait_time)
                
            return st.session_state.agent.get_response(prompt)
            
        except EventStreamError as e:
            if "throttlingException" in str(e):
                print(f"Rate limit hit, retrying with backoff: {str(e)}")
                raise  # This will trigger the retry
            raise  # Re-raise other EventStreamErrors

    def _process_successful_response(self, response: str) -> None:
        """
        Process a successful AI response.
        
        Args:
            response (str): The AI response to process
        """
        # Add the new message to chat history
        message_index = len(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Generate image with rate limiting
        try:
            with st.spinner("Generating image for the new response..."):
                if 'generated_images' not in st.session_state:
                    st.session_state.generated_images = {}
                
                # Add delay before image generation to prevent rate limiting
                time.sleep(1)
                image = st.session_state.image_service.generate_image(response)
                
                if image:
                    st.session_state.generated_images[message_index] = image
                else:
                    st.warning("Could not generate image for this response")
        except Exception as e:
            st.warning(f"Error generating image: {str(e)}")
            
        # Generate suggestions with rate limiting
        try:
            # Add delay before generating suggestions
            time.sleep(1)
            self._generate_suggestions(response)
        except Exception as e:
            st.warning(f"Error generating suggestions: {str(e)}")
            
        # Rerun if we have messages
        if st.session_state.messages:
            st.rerun()

    def _handle_user_input(self, prompt: str) -> None:
        """
        Process user input and get AI response with rate limiting and retries.
        
        Args:
            prompt (str): The user's input text
        """
        try:
            if not prompt or not isinstance(prompt, str):
                st.error("Invalid input. Please provide a valid text message.")
                return

            # Add user message to chat history
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Clear suggestions
            if 'suggestions' not in st.session_state:
                st.session_state.suggestions = []
            st.session_state.suggestions.clear()
            
            # Get AI response with retry mechanism
            response = None
            with st.spinner("Thinking..."):
                try:
                    response = self._get_ai_response_with_retry(prompt)
                    if not response:
                        st.warning("Received empty response from AI agent")
                        return
                except Exception as e:
                    st.error(f"Error getting AI response: {str(e)}")
                    return
                
            # Process response if successful
            if response:
                self._process_successful_response(response)

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

class RateLimiter:
    def __init__(self, tokens_per_second: float):
        self.tokens_per_second = tokens_per_second
        self.tokens = tokens_per_second
        self.last_update = time.time()

    def acquire(self) -> float:
        """
        Acquire a token and return the time to wait if necessary.
        
        Returns:
            float: Time to wait in seconds before proceeding
        """
        now = time.time()
        time_passed = now - self.last_update
        self.tokens = min(self.tokens_per_second,
                         self.tokens + time_passed * self.tokens_per_second)
        self.last_update = now

        if self.tokens < 1:
            return (1 - self.tokens) / self.tokens_per_second
        else:
            self.tokens -= 1
            return 0

def main():
    """
    Main entry point for the application.
    
    Initializes and runs the GameMasterUI.
    """
    app = GameMasterUI()
    app.run()


if __name__ == "__main__":
    main() 