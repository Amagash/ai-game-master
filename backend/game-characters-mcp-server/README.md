# D&D Character Management Service

This Spring Boot application provides a microservice for managing D&D game characters stored in Amazon DynamoDB.

## Overview

The service provides REST endpoints for creating, reading, updating, and deleting character data from a DynamoDB table.

## Prerequisites

- Java 17
- Maven
- AWS account with DynamoDB access
- AWS credentials configured locally

## Configuration

The application uses the following configuration properties in `application.properties`:

```properties
# AWS Configuration
aws.region=us-west-2
aws.dynamodb.table-name=genai-dnd-game-characters
```

You can modify these properties to match your AWS environment.

## DynamoDB Table Structure

The application expects a DynamoDB table with the following structure:
- Table name: Configured via `aws.dynamodb.table-name` property
- Partition key: `character_id`

## Character Model

The character model includes:
- Character ID (partition key as `character_id`)
- Character name (as `character_name`)
- Player ID (as `player_id`)
- Character class (as `class`)
- Race
- Gender
- Level and experience
- Stats (strength, dexterity, constitution, intelligence, wisdom, charisma)
- Inventory (list of items with `item_name` and `quantity`)
- Current status (as `current_status` with `hp`, `max_hp`, `condition`, and `buffs`)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /api/characters | Create a new character |
| GET    | /api/characters/{characterId} | Get a character by ID |
| GET    | /api/characters | Get all characters |
| PUT    | /api/characters/{characterId} | Update a character |
| DELETE | /api/characters/{characterId} | Delete a character |
| GET    | /api/characters/player/{playerId} | Get characters by player ID |
| POST   | /api/characters/{characterId}/experience | Add experience points to a character |
| GET    | /api/characters/{characterId}/progression | Get character progression information |

## Experience and Leveling

The application implements D&D 5e Basic Rules (2018) for experience points and character leveling:

- Characters automatically level up when they reach the XP threshold for the next level
- The AI Game Master can award XP through the `/experience` endpoint
- The progression endpoint provides information about current level, XP, and XP needed for next level

### XP Thresholds by Level

| Level | XP Required |
|-------|-------------|
| 1     | 0           |
| 2     | 300         |
| 3     | 900         |
| 4     | 2,700       |
| 5     | 6,500       |
| 6     | 14,000      |
| 7     | 23,000      |
| 8     | 34,000      |
| 9     | 48,000      |
| 10    | 64,000      |
| 11    | 85,000      |
| 12    | 100,000     |
| 13    | 120,000     |
| 14    | 140,000     |
| 15    | 165,000     |
| 16    | 195,000     |
| 17    | 225,000     |
| 18    | 265,000     |
| 19    | 305,000     |
| 20    | 355,000     |

## Building and Running

```bash
# Build the application
mvn clean package

# Run the application
java -jar target/characters-mcp-server-1.0.0-SNAPSHOT.jar
```

## AI Agent Integration

This service is designed to be invoked by an AI Agent via a tool. The AI Agent can use the REST endpoints to:
1. Create new characters
2. Retrieve character information
3. Update character stats, inventory, or status
4. Delete characters when needed
5. Award experience points and manage character progression

### Example: Adding Experience Points

```json
POST /api/characters/{characterId}/experience
{
  "experiencePoints": 300
}
```

### Example: Getting Progression Information

```
GET /api/characters/{characterId}/progression
```

Response:
```json
{
  "currentLevel": 2,
  "currentExperience": 450,
  "experienceForCurrentLevel": 300,
  "experienceForNextLevel": 900,
  "experienceNeeded": 450
}
```

## Example Character Creation Request

```json
POST /api/characters
{
  "characterName": "Elyndra",
  "playerId": "elyndra",
  "name": "Elyndra",
  "characterClass": "Wizard",
  "race": "Elf",
  "gender": "Female",
  "level": 1,
  "experience": 0,
  "stats": {
    "strength": 8,
    "dexterity": 14,
    "constitution": 12,
    "intelligence": 16,
    "wisdom": 13,
    "charisma": 10
  },
  "inventory": [
    {
      "itemName": "Spellbook",
      "quantity": 1
    },
    {
      "itemName": "Dagger",
      "quantity": 1
    }
  ],
  "currentStatus": {
    "hp": 8,
    "maxHp": 8,
    "condition": "Normal",
    "buffs": []
  }
}
```
