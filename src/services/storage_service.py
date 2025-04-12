import boto3
from src.config.aws_config import S3_CONFIG
from src.services.pdf_service import PDFService


class StorageService:
    """
    Service for storing game data in AWS S3.
    
    This class handles saving game sessions as PDF files to S3 buckets.
    """
    
    def __init__(self):
        """
        Initialize the StorageService with S3 client and bucket configuration.
        """
        self.s3_client = boto3.client('s3')
        self.bucket_name = S3_CONFIG['bucket_name']
    
    def save_game_session(self, messages, player_name):
        """
        Save game session as PDF to S3.
        
        Args:
            messages (list): List of message dictionaries containing the chat history
            player_name (str): Name of the player for filename generation
            
        Returns:
            tuple: (success, result) where success is a boolean indicating if the
                  operation was successful, and result is either the filename or
                  an error message
        """
        try:
            # Convert messages to PDF
            pdf_buffer = PDFService.create_chat_pdf(messages)

            player_id = player_name.lower().strip()
            
            # Generate filename
            filename = f"game_session_{player_id}.pdf"
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                pdf_buffer,
                self.bucket_name,
                f"game_sessions/{player_id}/{filename}",
                ExtraArgs={'ContentType': 'application/pdf'}
            )
            return True, filename
        except Exception as e:
            return False, str(e) 