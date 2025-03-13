# Game prompts for AI interactions

# Initial prompt to launch the game and set the scene
LAUNCH_PROMPT = """The player's name is {player_name} and you can welcome them to the game. 
The player is a {player_gender} {player_race} {player_class}.
Describe the surroundings of the player and create an atmosphere that the player can bounce off of. 
Don't make more than 100 words."""

# Prompt for generating player action suggestions
SUGGESTION_PROMPT = """You are a helpful game master assistant. Your task is to generate exactly 3 plausible and interesting actions that the player could take next in the game.

Player information:
- Name: {player_name}
- Gender: {player_gender}
- Race: {player_race}
- Class: {player_class}

Current game context:
{context}

IMPORTANT: Provide EXACTLY 3 short, specific action suggestions that would make sense in this context.
Format them as a numbered list with each suggestion being a short phrase or sentence (5-10 words) that the player could say or do.

For example:
1. Investigate the strange noise
2. Talk to the innkeeper about rumors
3. Search for hidden treasures

Your suggestions should be varied and interesting, giving the player meaningful choices.
DO NOT include any explanations or additional text - ONLY the numbered list of 3 suggestions.
"""


class ImagePrompts:
    """
    Collection of prompts and settings for image generation.
    
    This class provides static methods and constants for enhancing
    text prompts for better image generation results.
    """
    
    # Base styles and settings for consistent image generation
    BASE_STYLE = "heroic fantasy art style, detailed, vibrant colors, dramatic lighting, dungeon dragon"
    NEGATIVE_PROMPT = "text, watermark, signature, blurry, distorted, low quality"
    
    @staticmethod
    def enrich_prompt(text):
        """
        Enrich a text prompt with additional style information for better image generation.
        
        Args:
            text (str): The base text prompt
            
        Returns:
            dict: Formatted prompt with weights for positive and negative prompts
        """
        enhanced_text = f"{text}, {ImagePrompts.BASE_STYLE}"
        
        return {
            "text_prompts": [
                {"text": enhanced_text, "weight": 1.5},
                {"text": ImagePrompts.NEGATIVE_PROMPT, "weight": -1.0}
            ]
        }
