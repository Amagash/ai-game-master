import os

# DynamoDB configuration
DYNAMODB_CONFIG = {
    'table_name': os.environ.get('DYNAMODB_TABLE_NAME', 'game_characters'),
    'region': os.environ.get('AWS_REGION', 'us-west-2')
}

# DynamoDB table structure
TABLE_SCHEMA = {
    "TableName": "game_characters",
    "KeySchema": [
        {
            "AttributeName": "player_name",
            "KeyType": "HASH"
        },
        {
            "AttributeName": "character_name",
            "KeyType": "RANGE"
        }
    ],
    "AttributeDefinitions": [
        {
            "AttributeName": "player_name",
            "AttributeType": "S"
        },
        {
            "AttributeName": "character_name",
            "AttributeType": "S"
        }
    ],
    "ProvisionedThroughput": {
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }
} 