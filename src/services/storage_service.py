import boto3
from src.config.aws_config import S3_CONFIG
from src.services.pdf_service import PDFService

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = S3_CONFIG['bucket_name']
    
    def save_game_session(self, messages, player_name):
        """Save game session as PDF to S3"""
        try:
            # Convert messages to PDF
            pdf_buffer = PDFService.create_chat_pdf(messages)
            
            # Generate filename
            filename = f"game_session_{player_name}.pdf"
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                pdf_buffer,
                self.bucket_name,
                filename,
                ExtraArgs={'ContentType': 'application/pdf'}
            )
            return True, filename
        except Exception as e:
            return False, str(e) 