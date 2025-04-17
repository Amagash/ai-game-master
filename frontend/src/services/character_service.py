import boto3
from src.config.aws_config import DYNAMODB_CONFIG



class CharacterService:
    """
    Service for managing character data in DynamoDB.
    
    This class handles saving and retrieving character information,
    including stats, inventory, and status.
    """
    
    def __init__(self):
        """
        Initialize the CharacterService with DynamoDB connection.
        """
        self.dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_CONFIG['region'])
        self.table = self.dynamodb.Table(DYNAMODB_CONFIG['table_name'])

    def save_character(self, character_id, specs):
        """
        Save a character's specifications to DynamoDB.
        
        Args:
            character_id (str): Unique identifier for the character
            specs (dict): Character specifications including name, race, class, and stats
            
        Returns:
            bool: True if save was successful, False otherwise
            
        This method also adds default inventory and calculates derived stats
        like maximum hit points based on class and constitution.
        """
        try:
            # Default inventory for new characters
            default_inventory = [
                {"item_name": "Shortsword", "quantity": 1},
                {"item_name": "Shortbow", "quantity": 1},
                {"item_name": "Arrows", "quantity": 20},
                {"item_name": "Leather Armor", "quantity": 1},
                {"item_name": "Torch", "quantity": 2},
                {"item_name": "Flint & Tinder", "quantity": 1},
                {"item_name": "Rations", "quantity": 5},
                {"item_name": "Waterskin", "quantity": 1},
                {"item_name": "Map or Blank Parchment", "quantity": 1},
                {"item_name": "Quill & Ink", "quantity": 1},
                {"item_name": "Health Potion", "quantity": 1},
                {"item_name": "Gold Pieces", "quantity": 10}
            ]

            # Calculate max HP based on class and constitution
            base_hp = {
                "Barbarian": 12, "Fighter": 10, "Paladin": 10, "Ranger": 10,
                "Bard": 8, "Cleric": 8, "Druid": 8, "Monk": 8, "Rogue": 8, "Warlock": 8,
                "Sorcerer": 6, "Wizard": 6
            }.get(specs.get('class'), 8)
            
            constitution_modifier = (specs.get('Constitution', 10) - 10) // 2
            max_hp = base_hp + constitution_modifier

            # Ensure character_name is included as a key
            character_name = specs.get('character_name', '')
            if not character_name:
                raise ValueError("Character name is required")

            # Create the DynamoDB item with all character data
            self.table.put_item(
                Item={
                    "character_id": character_id,
                    "character_name": character_name,  # Add this as a key
                    "player_id": character_name.lower().strip(),  # Using character_name as player_id for now
                    "name": character_name,
                    "class": specs.get('class', ''),
                    "race": specs.get('race', ''),
                    "gender": specs.get('gender', ''),  # Add gender field
                    "level": 1,  # Starting at level 1
                    "experience": 0,  # Starting with 0 XP
                    "stats": {
                        "strength": specs.get('Strength', 10),
                        "dexterity": specs.get('Dexterity', 10),
                        "constitution": specs.get('Constitution', 10),
                        "intelligence": specs.get('Intelligence', 10),
                        "wisdom": specs.get('Wisdom', 10),
                        "charisma": specs.get('Charisma', 10)
                    },
                    "inventory": default_inventory,
                    "current_status": {
                        "hp": max_hp,
                        "max_hp": max_hp,
                        "condition": "Normal",
                        "buffs": []
                    }
                }
            )
            return True
        except Exception as e:
            print(f"Error saving character: {str(e)}")
            return False

    def get_character(self, character_id):
        """
        Retrieve a character's specifications from DynamoDB.
        
        Args:
            character_id (str): Unique identifier for the character
            
        Returns:
            dict: Character data if found, None otherwise
        """
        try:
            response = self.table.get_item(
                Key={'character_id': character_id}
            )
            return response.get('Item')
        except Exception as e:
            print(f"Error retrieving character: {str(e)}")
            return None 