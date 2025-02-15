import boto3
from src.config.aws_config import DYNAMODB_CONFIG

class CharacterService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_CONFIG['region'])
        self.table = self.dynamodb.Table(DYNAMODB_CONFIG['table_name'])

    def save_character(self, character_id, specs):
        """Save a character's specifications to DynamoDB"""
        try:
            self.table.put_item(
                Item={
                    'character_id': character_id,
                    'character_name': specs.get('character_name', ''),
                    'race': specs.get('race', ''),
                    'class': specs.get('class', ''),
                    'intelligence': specs.get('Intelligence', 0),
                    'strength': specs.get('Strength', 0),
                    'dexterity': specs.get('Dexterity', 0),
                    'constitution': specs.get('Constitution', 0),
                    'wisdom': specs.get('Wisdom', 0),
                    'charisma': specs.get('Charisma', 0),
                    # Add more attributes as needed
                }
            )
            return True
        except Exception as e:
            print(f"Error saving character: {str(e)}")
            return False

    def get_character(self, character_id):
        """Retrieve a character's specifications from DynamoDB"""
        try:
            response = self.table.get_item(
                Key={'character_id': character_id}
            )
            return response.get('Item')
        except Exception as e:
            print(f"Error retrieving character: {str(e)}")
            return None 