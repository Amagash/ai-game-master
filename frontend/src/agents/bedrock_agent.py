import boto3
import os
from dotenv import load_dotenv


class BedrockAgent:
    """
    Client for interacting with AWS Bedrock Agents.
    
    This class handles communication with the AWS Bedrock Agent service,
    allowing the application to send prompts and receive AI-generated responses.
    """
    
    def __init__(self):
        """
        Initialize the BedrockAgent with configuration from environment variables.
        
        Loads environment variables, validates required values, and sets up
        the Bedrock Agent client.
        """
        load_dotenv()
        self._validate_env_vars()
        self.agent_id = os.getenv('BEDROCK_AGENT_ID')
        self.agent_alias_id = os.getenv('BEDROCK_AGENT_ALIAS_ID')
        self.client = self._connect_to_bedrock()
    
    def _validate_env_vars(self):
        """
        Validate that all required environment variables are present.
        
        Raises:
            ValueError: If any required environment variables are missing
        """
        required_vars = ['AWS_REGION', 'BEDROCK_AGENT_ID', 'BEDROCK_AGENT_ALIAS_ID']
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    def _connect_to_bedrock(self):
        """
        Create and return a boto3 client for the Bedrock Agent runtime.
        
        Returns:
            boto3.client: Configured Bedrock Agent runtime client
        """
        return boto3.client(
            service_name='bedrock-agent-runtime',
            region_name=os.getenv('AWS_REGION')
        )
    
    def get_response(self, prompt, session_id="default-session"):
        """
        Send a prompt to the Bedrock Agent and get a response.
        
        Args:
            prompt (str): The text prompt to send to the agent
            session_id (str): Session identifier for conversation context
            
        Returns:
            str: The agent's response text, or None if no response
        """
        response = self.client.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias_id,
            sessionId=session_id,
            inputText=prompt
        )
        
        for event in response['completion']:
            if event.get('chunk'):
                return event['chunk']['bytes'].decode()
        return None 