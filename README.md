# AI Game Master

This project is a full-stack application with a frontend, backend, and infrastructure components. Below are the step-by-step instructions to get the project running locally.

## Prerequisites

- [Java 17](https://corretto.aws/downloads/latest/amazon-corretto-17-x64-macos-jdk.pkg) and follow the [instructions](https://docs.aws.amazon.com/corretto/latest/corretto-17-ug/macos-install.html)
- Maven 3.9.x (or use included wrapper)
- Node.js 16 or higher
- npm or yarn
- AWS CLI (for infrastructure deployment)
- Terraform (for infrastructure management)
- An AWS Account with appropriate permissions
- AWS Resources already deployed within your AWS Account (see [instructions here](./infrastructure/README.md))
- [Amazon Bedrock](https://aws.amazon.com/bedrock/?trk=b8f00cc8-e51d-4bfd-bf44-9b5ffb6acd1a&sc_channel=el)

## Project Structure

```
.
├── frontend/          # Frontend application
├── backend/          # Backend API and services
│   ├── game-characters-mcp-server/  # Spring Boot application
│   │   ├── src/                    # Source code
│   │   │   ├── config/            # AWS and application configuration
│   │   │   ├── model/             # Data models
│   │   │   ├── repository/        # DynamoDB data access
│   │   │   └── service/           # Business logic
│   │   └── pom.xml                # Maven configuration
│   └── mcp-inspector/              # MCP Inspector service
├── infrastructure/   # Infrastructure as Code
├── cloudformation/   # AWS CloudFormation templates
└── test/            # Test files
```

## Environment Variables

### Backend (.env)
Create a `.env` file in the `backend/game-characters-mcp-server` directory with the following variables:

```bash
# AWS Configuration
AWS_REGION=your_region
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key

# Application Configuration
SPRING_PROFILES_ACTIVE=dev
SERVER_PORT=8080

# DynamoDB Configuration
DYNAMODB_ENDPOINT=http://localhost:8000  # For local development
DYNAMODB_TABLE_NAME=table_name
```

### Frontend (.env)
Create a `.env` file in the `frontend` directory with the following variables:

```bash
# API Configuration
VITE_API_URL=http://localhost:8080
VITE_API_TIMEOUT=5000

# Feature Flags
VITE_ENABLE_DEBUG=true
VITE_ENABLE_ANALYTICS=false
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-game-master
```

### 2. AWS Configuration

1. Configure AWS credentials:
   ```bash
   aws configure
   ```

2. Export AWS credentials to environment variables:
   ```bash
   eval "$(aws configure export-credentials --profile [AWS-PROFILE] --format env)"
   ```

### 3. Backend Setup

1. Navigate to the Spring Boot application:
   ```bash
   cd backend/game-characters-mcp-server
   ```

2. Create and configure the environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials and configuration
   ```

3. Build the application using Maven:
   ```bash
   ./mvnw clean install
   ```

4. Run the application:
   ```bash
   ./mvnw spring-boot:run
   ```

### 4. Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install  # or yarn install
   ```

2. Create and configure the environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the development server:
   ```bash
   npm run dev  # or yarn dev
   ```

### 5. Infrastructure Setup

1. Initialize Terraform:
   ```bash
   cd infrastructure
   terraform init
   ```

2. Deploy infrastructure:
   ```bash
   terraform plan
   terraform apply
   ```

## Development

- Backend API runs on: http://localhost:8080
- Frontend development server runs on: http://localhost:3000

### Amazon DynamoDB Resources

The backend uses DynamoDB for data persistence with the following configuration:

- Table: dnd-genai-game-characters
  - Partition Key: character_id (String)
  - Attributes:
    - name (String)
    - level (Number)
    - experience (Number)
    - inventory (List)
    - stats (Map)
    - current_status (Map)

### AWS Configuration

- Region: us-west-2
- Authentication: DefaultCredentialsProvider
- Enhanced DynamoDB Client for improved type safety

## Testing

Run tests for each component:

```bash
# Backend tests
cd backend/game-characters-mcp-server
./mvnw test

# Frontend tests
cd frontend
npm test  # or yarn test
```

## Deployment

1. Build the frontend:
   ```bash
   cd frontend
   npm run build  # or yarn build
   ```

2. Deploy the backend:
   ```bash
   cd backend/game-characters-mcp-server
   ./mvnw clean package
   # Deploy the generated JAR file
   ```

3. Deploy infrastructure changes:
   ```bash
   cd infrastructure
   terraform apply
   ```

## Troubleshooting

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

3. Environment Variable Issues
   - Ensure all required environment variables are set
   - Check for typos in variable names
   - Verify the .env files are in the correct locations
   - For local development, ensure DynamoDB endpoint is correctly configured

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the terms of the license included in the repository.

## Support

For support, please open an issue in the repository or contact the maintainers. 
