# Game prompts
LAUNCH_PROMPT = """The player's name is {player_name} and you can welcome them to the game. 
The player is a {player_race} {player_class}.
Describe the surroundings of the player and create an atmosphere that the player can bounce off of."""

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
