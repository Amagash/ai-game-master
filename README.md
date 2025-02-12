# AI Game Master

An interactive text adventure game powered by AWS Bedrock and Streamlit.

## Description

AI Game Master is an interactive application that uses AI to create a unique role-playing experience. The application uses AWS Bedrock to generate contextual responses and create an immersive atmosphere for players.

## Features

- Interactive chat interface
- Contextual response generation via AWS Bedrock
- Game session saving to PDF in S3
- Intuitive user interface with Streamlit
- Custom dark theme

## Prerequisites

- Python 3.8+
- AWS account with Bedrock access
- Configured S3 bucket

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
pip install -e .
```

## Configuration

1. Create a `.env` file at the project root with the following variables:
```env
AWS_REGION=your-region
BEDROCK_AGENT_ID=your-agent-id
BEDROCK_AGENT_ALIAS_ID=your-agent-alias-id
S3_BUCKET_NAME=your-bucket-name
```

2. Ensure your AWS credentials are properly configured.

## Usage

Launch the application with:
```bash
streamlit run app.py
```

The application will be accessible at: http://localhost:8501

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
    ├── services/         # Services
    ├── config/           # Configuration
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

