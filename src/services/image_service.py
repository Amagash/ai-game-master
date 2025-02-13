import boto3
import base64
import json
from io import BytesIO
from src.config.prompts import ImagePrompts

class ImageService:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime')
        self.model_id = 'stability.stable-diffusion-xl-v1'

    def generate_image(self, text):
        """Generate an image from a text prompt"""
        try:
            # Get enriched prompt
            text_prompts = ImagePrompts.enrich_prompt(text)
            
            body = json.dumps({
                **text_prompts,  # Include enriched prompts
                "cfg_scale": 10,
                "steps": 50,
                "seed": 0
            })
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            image_b64 = response_body['artifacts'][0]['base64']
            
            return BytesIO(base64.b64decode(image_b64))
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return None 