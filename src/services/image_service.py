import boto3
import base64
import json
import io
import logging
from botocore.config import Config
from botocore.exceptions import ClientError
from src.config.prompts import ImagePrompts

class ImageError(Exception):
    """Custom exception for errors returned by Amazon Nova Canvas"""
    def __init__(self, message):
        self.message = message

class ImageService:
    def __init__(self):
        self.client = boto3.client(
            'bedrock-runtime',
            config=Config(read_timeout=300)
        )
        self.model_id = 'amazon.nova-canvas-v1:0'  # Using Amazon Nova Canvas
        self.llm_model_id = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'  # Claude 3.7 Sonnet for summarization
        self.logger = logging.getLogger(__name__)
        # Store character information
        self.character_info = None
    
    def set_character_info(self, character_info):
        """Set character information for image generation context"""
        self.character_info = character_info
        self.logger.info(f"Character info set: {character_info}")
    
    def _summarize_text(self, text, max_length=500):
        """Use Claude to generate a concise summary of the text for image generation"""
        try:
            if len(text) <= max_length:
                return text
            
            # Build character context if available
            character_context = ""
            if self.character_info:
                character_context = f"""
                Important character information:
                - Character: {self.character_info.get('character_name', 'Unknown')}
                - Gender: {self.character_info.get('gender', 'Unknown')}
                - Race: {self.character_info.get('race', 'Unknown')}
                - Class: {self.character_info.get('class', 'Unknown')}
                
                If the text describes the player character or refers to them, ensure the image description 
                maintains consistency with their gender, race, and class.
                """
                
            prompt = f"""
            I need a concise, vivid description for image generation based on the following text. 
            Focus on the visual elements and key details that would make a compelling image.
            Keep your response under 500 characters.
            
            {character_context}
            
            Text to summarize:
            {text}
            
            Concise image description:
            """
            
            # Prepare the request for Claude
            request_body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
            
            # Invoke Claude
            response = self.client.invoke_model(
                modelId=self.llm_model_id,
                body=request_body,
                accept="application/json",
                contentType="application/json"
            )
            
            # Parse the response
            response_body = json.loads(response.get("body").read())
            summary = response_body.get("content", [{}])[0].get("text", "")
            
            # Clean up the summary
            summary = summary.strip()
            
            self.logger.info(f"Generated summary for image prompt: {summary[:50]}...")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error summarizing text: {str(e)}")
            # Fall back to simple truncation if summarization fails
            return text[:max_length-3] + "..."

    def generate_image(self, text):
        """Generate an image from a text prompt using Nova Canvas"""
        try:
            self.logger.info(f"Generating image with Amazon Nova Canvas model {self.model_id}")
            
            # Generate a concise summary for image generation
            image_prompt = self._summarize_text(text)
            
            # Format the request for Nova Canvas
            body = json.dumps({
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": image_prompt
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "height": 1024,
                    "width": 1024,
                    "cfgScale": 8.0,
                    "seed": 0
                }
            })
            
            # Invoke the model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
                accept="application/json",
                contentType="application/json"
            )
            
            # Process the response
            response_body = json.loads(response.get("body").read())
            
            # Check for errors
            error = response_body.get("error")
            if error is not None:
                raise ImageError(f"Image generation error: {error}")
            
            # Extract and decode the image
            base64_image = response_body.get("images")[0]
            base64_bytes = base64_image.encode('ascii')
            image_bytes = base64.b64decode(base64_bytes)
            
            self.logger.info(f"Successfully generated image with Amazon Nova Canvas model {self.model_id}")
            
            # Return as BytesIO for Streamlit to display
            return io.BytesIO(image_bytes)
            
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", "Unknown error")
            self.logger.error(f"Client error: {error_code} - {error_message}")
            print(f"Error generating image: {error_code} - {error_message}")
            return None
        except ImageError as e:
            self.logger.error(e.message)
            print(f"Image generation error: {e.message}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            print(f"Unexpected error generating image: {str(e)}")
            return None 