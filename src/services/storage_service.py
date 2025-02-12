import boto3
from src.config.aws_config import S3_CONFIG

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = S3_CONFIG['bucket_name']
    
    def save_game_session(self, pdf_buffer, player_name):
        filename = f"game_session_{player_name}.pdf"
        try:
            self.s3_client.upload_fileobj(
                pdf_buffer,
                self.bucket_name,
                filename,
                ExtraArgs={'ContentType': 'application/pdf'}
            )
            return True, filename
        except Exception as e:
            return False, str(e) 