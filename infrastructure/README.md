# D&D GenAI Infrastructure: AI-Powered Dungeons & Dragons Game Master Platform

This project provides an AWS-based infrastructure for an AI-powered Dungeons & Dragons game management system. It leverages Amazon Bedrock to create an intelligent game master that combines specialized knowledge of D&D rules with dynamic NPC interactions and game flow management.

The system uses multiple specialized AI agents working in collaboration to provide a comprehensive D&D gaming experience. The infrastructure includes a rules-focused knowledge base, dedicated agents for rules arbitration and NPC interactions, and a supervisor agent that acts as the game master, orchestrating the overall game flow and player interactions.

## Data Flow
The system processes D&D game sessions through a multi-agent collaboration system.

```ascii
[Player Input] -> [Game Master Agent]
       |               |
       v               v
[Rules Agent] <-> [NPC Agent]
       |               |
       v               v
[Knowledge Base] [Character API]
```

Component Interactions:
1. Game Master Agent receives player input and coordinates responses
2. Rules Agent validates actions against D&D ruleset stored in Knowledge Base
3. NPC Agent manages non-player character interactions and behaviors
4. Knowledge Base provides rule reference and game context
5. Character API handles game state persistence and character management
6. Agents communicate using Bedrock Agent Runtime protocols
7. S3 stores static game assets and knowledge base data

## Repository Structure
```
infrastructure/
├── bin/
│   └── infra.ts                 # Entry point for CDK app deployment
├── lib/
│   ├── config.ts                # Lambda configuration and shared settings
│   └── dnd-genai-stack.ts       # Main infrastructure stack definition
├── resources/
│   ├── action-group-test-event.json              # Test event templates
│   └── game-characters-openapi-actions-group.yaml # API specification for character management
├── test/
│   └── infra.test.ts           # Infrastructure test suite
├── cdk-deploy-to.sh            # Deployment script for AWS environments
├── cdk-destroy-from.sh         # Cleanup script for AWS resources
├── cdk.json                    # CDK configuration and context
└── package.json                # Project dependencies and scripts
```

## Usage Instructions
### Prerequisites
- Node.js (v14.x or later)
- AWS CDK CLI installed (`npm install -g aws-cdk`)
- An AWS account with permissions to create:
  - Amazon Bedrock resources
  - Amazon S3 buckets
  - AWS IAM Roles and Policies
- **AWS CLI configured with appropriate credentials** (`aws configure`)

### Installation

1. Clone the repository and install dependencies:
```bash
git clone <repository-url>
cd infrastructure
npm install
```

2. Deploy the infrastructure:
```bash
./cdk-deploy-to.sh [DEV_ENV] [AWS_ACCOUNT_ID] [AWS_REGION_ID] (optional)[AWS_PROFILE_NAME]
```

3. Configure & Launch the web application with values from deployment outputs (see [instructions here](./../frontend/README.md))

### Troubleshooting

Common Issues:

1. Permission Issues
```
User is not authorized to perform: bedrock:CreateAgent
```
Solution:
- Ensure your [AWS-PROFILE] have the necessary permissions
- Add the required IAM policies to your role/user

2. Deployment Failures
- Check CloudWatch Logs for detailed error messages
- Verify that all required services are enabled in your AWS account
- Ensure your AWS account limits can accommodate the resources

## Cleanup
In order to delete created stack(s), run the following command:
```bash
./cdk-destroy-from.sh [DEV_ENV] [AWS_ACCOUNT_ID] [AWS_REGION_ID] (optional)[AWS_PROFILE_NAME]
```