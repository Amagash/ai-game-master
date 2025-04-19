# Game Characters Management Service - A Spring Boot DynamoDB-backed Character Service

This Spring Boot application provides a robust microservice for managing game characters with DynamoDB persistence. It offers comprehensive character management features including experience tracking, level progression, and inventory management through MCP tools.

The service is built using Spring Boot and integrates with AWS DynamoDB for data persistence. It provides tools for character creation, updates, and progression tracking while maintaining character state and inventory. The service is designed to be part of a larger game system, exposing its functionality through Spring AI Tool annotations for seamless integration with AI-powered game features.

## Repository Structure
```
backend/game-characters-mcp-server/
├── mvnw                    # Maven wrapper script for Unix systems
├── mvnw.cmd               # Maven wrapper script for Windows
├── pom.xml                # Maven project configuration
└── src/
    └── main/
        ├── java/com/characters/
        │   ├── config/
        │   │   └── DynamoDBConfig.java       # AWS DynamoDB configuration
        │   ├── GameCharactersApplication.java # Main application entry point
        │   ├── model/                        # Data model classes
        │   │   ├── CurrentStatus.java        # Character status tracking
        │   │   ├── GameCharacters.java       # Main character entity
        │   │   ├── InventoryItem.java        # Character inventory items
        │   │   └── Stats.java                # Character statistics
        │   ├── repository/
        │   │   └── CharacterRepository.java   # DynamoDB data access
        │   └── service/
        │       ├── CharacterService.java      # Character management logic
        │       └── ExperienceService.java     # Experience/leveling system
        └── resources/
            └── application.properties         # Application configuration
```

## Usage Instructions
### Prerequisites
- Java 17 or later
- AWS Account with DynamoDB access
- AWS CLI configured with appropriate credentials
- Maven 3.9.x (or use included wrapper)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend/game-characters-mcp-server
```

2. Configure AWS credentials (if not already done):
```bash
aws configure
```

3. Build the application:
```bash
./mvnw clean install
```

4. Containerize the application:
```bash
./mvnw spring-boot:build-image -Dspring-boot.build-image.imageName=game-characters-mcp-server
```

### Quick Start

1. Start the application:
```bash
./mvnw spring-boot:run
```

### Troubleshooting

1. DynamoDB Connection Issues
- Error: "Unable to connect to DynamoDB"
- Solution: 
  ```bash
  aws sts get-caller-identity  # Verify AWS credentials
  ```
- Check region configuration in application.properties

2. Character Updates Not Persisting
- Enable debug logging in application.properties:
  ```properties
  logging.level.com.characters=DEBUG
  ```
- Verify DynamoDB table permissions

## Data Flow
The service handles character data through a structured flow from API to persistence layer.

```ascii
Client Request → CharacterService → CharacterRepository → DynamoDB
     ↑                  ↓                    ↑              ↓
     └──────────Response──────────────Data Object────────Storage
```

Key component interactions:
1. CharacterService processes business logic and validates requests
2. ExperienceService handles level progression calculations
3. CharacterRepository manages DynamoDB operations
4. DynamoDB stores character data with partition key on characterId
5. Spring AI Tool annotations expose functions for AI integration

### Amazon DynamoDB Resources
- Table: dnd-mcp-game-characters
  - Partition Key: characterId (String)
  - Attributes:
    - name (String)
    - level (Number)
    - experience (Number)
    - inventory (List)
    - stats (Map)
    - currentStatus (Map)

### AWS Configuration
- Region: us-west-2
- Authentication: DefaultCredentialsProvider
- Enhanced DynamoDB Client for improved type safety