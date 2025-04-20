# AI Game Master

AI Game Master is an interactive application that uses AI to create a unique role-playing experience. The application uses Amazon Bedrock to generate contextual responses and create an immersive atmosphere for players. It features character creation, dynamic storytelling, and AI-generated images that match the narrative.

## Game Play

- Use the chat interface to interact with the AI Game Master
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

## Usage Instructions
### Prerequisites
- Python 3.8+
- AWS account with Amazon Bedrock access
  - Access to Claude models for text generation
  - Access to Nova Canvas for image generation
You can enable these models in the Amazon Bedrock console under "Model access" (see left pane).

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frontend
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

### Configuration

1. Create a `.env` file at the project root with the following variables with values from [infrastructure](./../infrastructure/README.md#installation) deployment outputs:
```env
AWS_REGION=your-region
BEDROCK_AGENT_ID=your-agent-id
BEDROCK_AGENT_ALIAS_ID=your-agent-alias-id
S3_BUCKET_NAME=your-bucket-name
DYNAMODB_TABLE_NAME=your-table-name
```

### Quick Start

1. Exports AWS credentials from your `[AWS-PROFILE]` profile to environment variables:
```bash
eval "$(aws configure export-credentials --profile [AWS-PROFILE] --format env)"
```

2. Launch the application using the following command:
```bash
streamlit run app.py
```

The application will be accessible at: http://localhost:8501

### Troubleshooting

1. AWS Credentials Issues:
   ```bash
   botocore.exceptions.NoCredentialsError: Unable to locate credentials
   ```
   - Ensure AWS credentials are properly exported
   - Verify AWS profile exists and has correct permissions
   - Check if credentials have expired

2. Bedrock Model Access:
   ```
   ClientError: An error occurred (AccessDeniedException) when calling the InvokeModel operation
   ```
   - Verify Amazon Bedrock model access is enabled in AWS console
   - Ensure IAM role has bedrock:InvokeModel permissions
   - Check if selected region has the required models available

3. Environment Configuration:
   - Verify all required environment variables are set in .env file
   - Check if S3 bucket and DynamoDB table names match infrastructure outputs
