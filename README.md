# AI Game Master

An interactive text adventure game powered by [AWS Bedrock](https://aws.amazon.com/bedrock/?trk=b8f00cc8-e51d-4bfd-bf44-9b5ffb6acd1a&sc_channel=el) and Streamlit.

## Description

AI Game Master is an interactive application that uses AI to create a unique role-playing experience. The application uses [AWS Bedrock](https://aws.amazon.com/bedrock/?trk=b8f00cc8-e51d-4bfd-bf44-9b5ffb6acd1a&sc_channel=el) to generate contextual responses and create an immersive atmosphere for players. It features character creation, dynamic storytelling, and AI-generated images that match the narrative.

## Features

- Interactive chat interface with AI game master
- Comprehensive character creation system with race, class, gender, and stats
- Contextual response generation via [AWS Bedrock](https://aws.amazon.com/bedrock/?trk=b8f00cc8-e51d-4bfd-bf44-9b5ffb6acd1a&sc_channel=el)
- AI-generated images using [Amazon Nova Canvas](https://aws.amazon.com/ai/generative-ai/nova/creative/?trk=b8f00cc8-e51d-4bfd-bf44-9b5ffb6acd1a&sc_channel=el)
- Intelligent image prompting that maintains character consistency
- Game session saving to PDF in S3
- Character data storage in [DynamoDB](https://aws.amazon.com/pm/dynamodb/?trk=b8f00cc8-e51d-4bfd-bf44-9b5ffb6acd1a&sc_channel=el)
- Intuitive user interface with Streamlit
- Custom dark theme
- Clickable action suggestions for player guidance
- Image caching to improve performance

## AWS Bedrock Agent Integration

The application uses a pre-configured AWS Bedrock Agent that enhances the game experience through:

- **Knowledge Bases**: The agent has access to knowledge bases containing game lore, rules, and world information, allowing it to provide rich, consistent responses about the game world.

- **Lambda Functions**: The agent can trigger Lambda functions to execute game mechanics like:
  - Dice rolling for skill checks and combat
  - Character action resolution
  - Game state management

- **Action Groups**: The agent is configured with action groups that define what operations it can perform, ensuring it can properly interpret player intentions and execute appropriate game actions.

This integration allows the AI Game Master to not only generate narrative content but also understand and implement game mechanics without requiring additional code in the application itself.

## Prerequisites

- Python 3.8+
- AWS account with Bedrock access
  - Access to Claude models for text generation
  - Access to Nova Canvas for image generation
- Configured S3 bucket for game session storage
- DynamoDB table for character data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Amagash/ai-game-master.git
cd ai-game-master
```

2. Create and activate a virtual environment:
```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

## Configuration

1. Create a `.env` file at the project root with the following variables:
```env
AWS_REGION=your-region
BEDROCK_AGENT_ID=your-agent-id
BEDROCK_AGENT_ALIAS_ID=your-agent-alias-id
S3_BUCKET_NAME=your-bucket-name
DYNAMODB_TABLE_NAME=your-table-name
```

2. Configure your AWS credentials using one of these methods:

   a. Using AWS CLI (recommended):
   ```bash
   aws configure
   ```
   Then enter your:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region name
   - Default output format (json)

   b. Or manually create/edit `~/.aws/credentials`:
   ```ini
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   ```

   And `~/.aws/config`:
   ```ini
   [default]
   region = your-region
   output = json
   ```

## AWS Bedrock Model Access

Ensure your AWS account has access to the following models:
- Claude 3 Sonnet (for text generation and summarization)
- Amazon Nova Canvas (for image generation)

You can enable these models in the AWS Bedrock console under "Model access".

## Usage

Launch the application with:
```bash
streamlit run app.py
```

The application will be accessible at: http://localhost:8501

### Character Creation

1. Enter your character's name
2. Select your character's race, class, and gender
3. Adjust ability scores as desired
4. Click "Start Adventure" to begin your journey

### Game Play

- Use the chat interface to interact with the AI Game Master
- Click on suggested actions or type your own responses
- Images will be generated based on the narrative
- Character information is displayed in the sidebar
- Save your game session using the "Save Game" button

## Project Structure

```
ai-game-master/
├── app.py                # Entry point
├── setup.py              # Package configuration
├── requirements.txt      # Dependencies
├── .env                  # Environment variables (not versioned)
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── src/
    ├── agents/           # Bedrock interaction logic
    ├── services/         # Services (image, character, storage)
    ├── config/           # Configuration and prompts
    └── ui/               # Streamlit user interface
```

## Contributing

Contributions are welcome! Feel free to:
1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

[Apache 2.0](LICENSE)

