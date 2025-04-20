/***** CDK *****/
import { Construct } from 'constructs';
import { Stack, StackProps, RemovalPolicy, CfnOutput, Tags } from 'aws-cdk-lib';
/***** END CDK *****/

import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { BucketDeployment, Source } from 'aws-cdk-lib/aws-s3-deployment';
import { bedrock } from '@cdklabs/generative-ai-cdk-constructs';
import { join } from 'path';

export class DNDGenAIStack extends Stack {

    private _appResourcePrefix: string = 'dnd-genai';
    private _kbS3Prefix: string = '';
    private _kbInstruction: string = '';
    private _rulesInstruction: string = '';
    private _npcInstruction: string = '';
    private _supervisorInstruction: string = '';
    private _collabWRulesInstruction: string = '';
    private _collabWNPCInstruction: string = '';

    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);
        const config: any = this.getConfig();
        if (config !== undefined) {
            this._kbS3Prefix = config['kb_s3_prefix'];
            this._kbInstruction = config['kb_instruction'];
            this._rulesInstruction = config['rules_instruction'];
            this._npcInstruction = config['npc_instruction'];
            this._supervisorInstruction = config['supervisor_instruction'];
            this._collabWRulesInstruction = config['supervisor_collab_with_rules_instruction'];
            this._collabWNPCInstruction = config['supervisor_collab_with_npc_instruction'];

            // Create a specialized Knowledge Base on D&D rules
            const bucketWAssets: s3.Bucket = this.createBucket(`${this._appResourcePrefix}-game-assets`);
            new BucketDeployment(this, 'DNDBucketDeployment', {
                sources: [Source.asset(join(__dirname, '../data/'))],
                destinationBucket: bucketWAssets,
                destinationKeyPrefix: this._kbS3Prefix,
            });
            const rulesKB: bedrock.VectorKnowledgeBase = this.createBedrockVectorKB(this._kbInstruction);
            this.createBedrockKBDataSource(rulesKB, bucketWAssets, this._kbS3Prefix);

            // Create a specialized agent for D&D rules
            const rulesAgent: bedrock.Agent = new bedrock.Agent(this, 'DNDRulesAgent', {
                name: `${this._appResourcePrefix}-rules-agent`,
                foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_HAIKU_V1_0,
                knowledgeBases: [rulesKB],
                instruction: this._rulesInstruction,
                shouldPrepareAgent: true,
            });
            const rulesAgentAlias = new bedrock.AgentAlias(this, 'DNDRulesAgentAlias', {
                agent: rulesAgent,
                aliasName: 'dnd-rules',
            });

            // Create a specialized agent for NPC interactions with Players
            const npcAgent: bedrock.Agent = new bedrock.Agent(this, 'DNDNPCAgent', {
                name: `${this._appResourcePrefix}-npc-agent`,
                foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_SONNET_V1_0,
                instruction: this._npcInstruction,
                shouldPrepareAgent: true,
            });
            const npcAgentAlias = new bedrock.AgentAlias(this, 'DNDNPCAgentAlias', {
                agent: npcAgent,
                aliasName: 'dnd-npc',
            });

            // Create a Game Master agent that can collaborate with the specialized agents
            const gameMasterAgent = new bedrock.Agent(this, 'DNDGameMasterAgent', {
                name: `${this._appResourcePrefix}-game-master-agent`,
                foundationModel: bedrock.BedrockFoundationModel.ANTHROPIC_CLAUDE_3_5_HAIKU_V1_0,
                userInputEnabled: true,
                instruction: this._supervisorInstruction,
                shouldPrepareAgent: true,
                agentCollaboration: bedrock.AgentCollaboratorType.SUPERVISOR,
                agentCollaborators: [
                    new bedrock.AgentCollaborator({
                        collaboratorName: `${this._appResourcePrefix}-rules-collaborator`,
                        agentAlias: rulesAgentAlias,
                        collaborationInstruction: this._collabWRulesInstruction,
                        relayConversationHistory: false
                    }),
                    new bedrock.AgentCollaborator({
                        collaboratorName: `${this._appResourcePrefix}-npc-collaborator`,
                        agentAlias: npcAgentAlias,
                        collaborationInstruction: this._collabWNPCInstruction,
                        relayConversationHistory: true
                    }),
                ],
            });
            const gameMasterAgentAlias = new bedrock.AgentAlias(this, 'DNDGameMasterAgentAlias', {
                agent: gameMasterAgent,
                aliasName: 'dnd-gm',
            });

            // Create a DynamoDB table to store game characters' specifications
            const charactersTable = new dynamodb.Table(this, 'DNDCharactersTable', {
                tableName: `${this._appResourcePrefix}-game-characters`,
                partitionKey: { name: 'character_id', type: dynamodb.AttributeType.STRING },
                removalPolicy: RemovalPolicy.DESTROY,
                billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
            });

            // Outputs
            new CfnOutput(this, 'DNDAWSRegion', {
                value: props?.env?.region || '',
                exportName: 'DNDAWSRegion',
            });
            new CfnOutput(this, 'DNDGameMasterAgentId', {
                value: gameMasterAgent.agentId,
                exportName: 'DNDGameMasterAgentId',
            });
            new CfnOutput(this, 'DNDGameMasterAgentAliasId', {
                value: gameMasterAgentAlias.aliasId || '',
                exportName: 'DNDGameMasterAgentAliasId',
            });
            new CfnOutput(this, 'DNDCharactersTableName', {
                value: charactersTable.tableName,
                exportName: 'DNDCharactersTableName',
            });
            new CfnOutput(this, 'DNDGameAssetsBucketName', {
                value: bucketWAssets.bucketName,
                exportName: 'DNDGameAssetsBucketName',
            });
        }
    }

    // Getting config defined into cdk.json
    // and passing it to the stack
    private getConfig(): any {
        return this.node.tryGetContext('config')['dnd'];
    }

    private createBucket(bucketName: string): s3.Bucket {
        const bucketNameID = bucketName.replace('-', '').toUpperCase();
        return new s3.Bucket(this, bucketNameID, {
            bucketName: bucketName.toLowerCase(),
            autoDeleteObjects: true,
            encryption: s3.BucketEncryption.S3_MANAGED,
            removalPolicy: RemovalPolicy.DESTROY,
        });
    }

    private createBedrockVectorKB(kbInstruction: string): bedrock.VectorKnowledgeBase {
        const vectorKB = new bedrock.VectorKnowledgeBase(this, 'DNDBedrockVectorKB', {
            name: this._appResourcePrefix + '-kb',
            embeddingsModel: bedrock.BedrockFoundationModel.COHERE_EMBED_ENGLISH_V3,
            instruction: kbInstruction
        });
        Tags.of(vectorKB).add('mcp-multirag-kb', 'true');

        return vectorKB;
    }

    private createBedrockKBDataSource(kb: bedrock.VectorKnowledgeBase, kbBucket: s3.Bucket, kbPrefix?: string): bedrock.S3DataSource {
        return new bedrock.S3DataSource(this, 'DNDS3DataSource', {
            dataSourceName: this._appResourcePrefix + '-rules',
            knowledgeBase: kb,
            bucket: kbBucket,
            inclusionPrefixes: [kbPrefix || "/"],
            chunkingStrategy: bedrock.ChunkingStrategy.FIXED_SIZE,
        });
    }
}