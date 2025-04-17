import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# General AWS configuration
AWS_CONFIG = {
    'region': os.getenv('AWS_REGION', 'us-west-2'),  # Default to us-west-2 if not specified
}

# S3 bucket configuration for storing game sessions
S3_CONFIG = {
    'bucket_name': os.getenv('S3_BUCKET_NAME', 'dnd-genai-game-assets') # Default bucket name
}

# DynamoDB configuration for storing character data
DYNAMODB_CONFIG = {
    'table_name': os.getenv('DYNAMODB_TABLE_NAME', 'dnd-mcp-game-characters'),  # Default table name
    'region': AWS_CONFIG['region']  # Use the same region as general AWS config
} 