import boto3
import os
from dotenv import load_dotenv

class BedrockAgent:
    def __init__(self):
        load_dotenv()
        self._validate_env_vars()
        self.agent_id = os.getenv('BEDROCK_AGENT_ID')
        self.agent_alias_id = os.getenv('BEDROCK_AGENT_ALIAS_ID')
        self.client = self._connect_to_bedrock()
    
    def _validate_env_vars(self):
        required_vars = ['AWS_REGION', 'BEDROCK_AGENT_ID', 'BEDROCK_AGENT_ALIAS_ID']
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    def _connect_to_bedrock(self):
        return boto3.client(
            service_name='bedrock-agent-runtime',
            region_name=os.getenv('AWS_REGION')
        )
    
    def get_response(self, prompt, session_id="default-session"):
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