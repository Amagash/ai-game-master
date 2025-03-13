# Game prompts
LAUNCH_PROMPT = """The player's name is {player_name} and you can welcome them to the game. 
The player is a {player_gender} {player_race} {player_class}.
Describe the surroundings of the player and create an atmosphere that the player can bounce off of. 
Don't make more than 100 words."""

# Suggestion prompt for generating player action options
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

# Image generation prompts
class ImagePrompts:
    # Base styles and settings
    BASE_STYLE = "heroic fantasy art style, detailed, vibrant colors, dramatic lighting, dungeon dragon"
    NEGATIVE_PROMPT = "text, watermark, signature, blurry, distorted, low quality"
    
    @staticmethod
    def enrich_prompt(text):
        """Enrich the prompt for better image generation"""
        enhanced_text = f"{text}, {ImagePrompts.BASE_STYLE}"
        
        return {
            "text_prompts": [
                {"text": enhanced_text, "weight": 1.5},
                {"text": ImagePrompts.NEGATIVE_PROMPT, "weight": -1.0}
            ]
        }
