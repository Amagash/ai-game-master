import boto3
import base64
import json
from io import BytesIO

class ImageService:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime')
        self.model_id = 'stability.stable-diffusion-xl-v1'

    def generate_image(self, prompt):
        """Generate an image from a text prompt"""
        try:
            body = json.dumps({
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 10,
                "steps": 50,
                "seed": 0,
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