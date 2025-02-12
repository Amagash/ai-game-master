import os
from dotenv import load_dotenv

load_dotenv()

AWS_CONFIG = {
    'region': os.getenv('AWS_REGION', 'us-west-2'),
}

S3_CONFIG = {
    'bucket_name': os.getenv('S3_BUCKET_NAME')
}

DYNAMODB_CONFIG = {
    'table_name': os.getenv('DYNAMODB_TABLE_NAME', 'game_characters'),
    'region': AWS_CONFIG['region']
} 