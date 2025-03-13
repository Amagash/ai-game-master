# Game prompts
LAUNCH_PROMPT = """The player's name is {player_name} and you can welcome them to the game. 
The player is a {player_gender} {player_race} {player_class}.
Describe the surroundings of the player and create an atmosphere that the player can bounce off of."""

# Suggestion prompt for generating player action options
SUGGESTION_PROMPT = """Based on the current game context, generate 3 plausible and interesting actions that the player could take next.
The player is a {player_gender} {player_race} {player_class} named {player_name}.

Current game context:
{context}

Provide exactly 3 short, specific action suggestions that would make sense in this context. 
Format them as a numbered list (1., 2., 3.) with each suggestion being a short phrase or sentence that the player could say or do.
Make sure the suggestions are varied and interesting, giving the player meaningful choices.
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
