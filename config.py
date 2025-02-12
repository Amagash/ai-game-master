import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS Bedrock Agent Configuration
BEDROCK_CONFIG = {
    'region': os.getenv('AWS_REGION'),
    'agent_id': os.getenv('BEDROCK_AGENT_ID'),
    'agent_alias_id': os.getenv('BEDROCK_AGENT_ALIAS_ID')
} 

# AWS S3 Configuration
S3_CONFIG = {
    'bucket_name': os.getenv('S3_BUCKET_NAME')
}