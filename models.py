import boto3
from datetime import datetime
from db_config import DYNAMODB_CONFIG

class Character:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(DYNAMODB_CONFIG['table_name'])
    
    def save_character(self, character_data):
        """
        Save or update a character
        character_data should include:
        - player_name: string
        - character_name: string
        - attributes: dict (strength, dexterity, etc.)
        - class: string
        - race: string
        - inventory: list
        - skills: list
        etc.
        """
        item = {
            'player_name': character_data['player_name'],
            'character_name': character_data['character_name'],
            'created_at': datetime.now().isoformat(),
            'attributes': character_data.get('attributes', {}),
            'character_class': character_data.get('class', ''),
            'race': character_data.get('race', ''),
            'inventory': character_data.get('inventory', []),
            'skills': character_data.get('skills', []),
            'level': character_data.get('level', 1),
            'experience': character_data.get('experience', 0)
        }
        
        try:
            self.table.put_item(Item=item)
            return True
        except Exception as e:
            print(f"Error saving character: {str(e)}")
            return False
    
    def get_character(self, player_name, character_name):
        """Retrieve a character"""
        try:
            response = self.table.get_item(
                Key={
                    'player_name': player_name,
                    'character_name': character_name
                }
            )
            return response.get('Item')
        except Exception as e:
            print(f"Error retrieving character: {str(e)}")
            return None
    
    def update_character(self, player_name, character_name, updates):
        """Update specific character attributes"""
        update_expression = "SET "
        expression_values = {}
        
        for key, value in updates.items():
            update_expression += f"#{key} = :{key}, "
            expression_values[f":{key}"] = value
        
        update_expression = update_expression.rstrip(", ")
        
        try:
            self.table.update_item(
                Key={
                    'player_name': player_name,
                    'character_name': character_name
                },
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames={f"#{k}": k for k in updates.keys()}
            )
            return True
        except Exception as e:
            print(f"Error updating character: {str(e)}")
            return False 