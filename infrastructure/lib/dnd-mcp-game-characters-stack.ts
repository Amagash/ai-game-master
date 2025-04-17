/***** CDK *****/
import { Construct } from 'constructs';
import { Stack, StackProps, Duration, RemovalPolicy, CfnOutput } from 'aws-cdk-lib';
/***** END CDK *****/

import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { bedrock } from '@cdklabs/generative-ai-cdk-constructs';
import * as lambda from "aws-cdk-lib/aws-lambda";
import { join } from 'path';

import { type LambdaProps, lambdaConfig } from './config';

export class GameCharactersMCPServerStack extends Stack {

    private _appResourcePrefix: string = 'dnd-mcp';

    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        // const containerPort = 8081;
        // const gcServiceName = this._appResourcePrefix + '-game-characters-service';

        // // Create VPC
        // const vpc = new ec2.Vpc(this, 'GCVPC', {
        //     maxAzs: 2,
        //     subnetConfiguration: [
        //         {
        //             cidrMask: 24,
        //             name: 'Public',
        //             subnetType: ec2.SubnetType.PUBLIC,
        //         }
        //     ],
        // });

        // // Create ECS Cluster
        // const cluster = new ecs.Cluster(this, 'GCECSCluster', {
        //     vpc,
        //     clusterName: `${this._appResourcePrefix}-gc-cluster`,
        // });

        // // Create Log Group
        // const logGroup = new logs.LogGroup(this, 'GCLogGroup', {
        //     logGroupName: `/ecs/${Stack.of(this).stackName}`,
        //     removalPolicy: RemovalPolicy.DESTROY,
        //     retention: logs.RetentionDays.ONE_DAY,
        // });

        // // Create Task Role
        // const taskRole = new iam.Role(this, 'GCTaskRole', {
        //     assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
        // });

        // // Create Task Definition
        // const taskDefinition = new ecs.FargateTaskDefinition(this, 'GCTaskDefinition', {
        //     memoryLimitMiB: 512,
        //     cpu: 256,
        //     taskRole,
        //     family: gcServiceName,
        // });

        // // Add Container to Task Definition
        // const container = taskDefinition.addContainer('GCServiceContainer', {
        //     image: ecs.ContainerImage.fromRegistry('game-characters-mcp-server:latest'),
        //     logging: ecs.LogDriver.awsLogs({
        //         logGroup,
        //         streamPrefix: 'gc-ecs',
        //     }),
        // });

        // container.addPortMappings({
        //     containerPort,
        // });

        // // Create Security Groups
        // const lbSecurityGroup = new ec2.SecurityGroup(this, 'GCLoadBalancerSecurityGroup', {
        //     vpc,
        //     description: 'Security group for ALB',
        //     allowAllOutbound: true,
        // });

        // lbSecurityGroup.addIngressRule(
        //     ec2.Peer.ipv4("87.89.176.179/32"),
        //     ec2.Port.tcp(80),
        //     'Allow inbound HTTP traffic'
        // );

        // const containerSecurityGroup = new ec2.SecurityGroup(this, 'GCContainerSecurityGroup', {
        //     vpc,
        //     description: 'Security group for container',
        //     allowAllOutbound: true,
        // });

        // containerSecurityGroup.addIngressRule(
        //     ec2.Peer.securityGroupId(lbSecurityGroup.securityGroupId),
        //     ec2.Port.tcp(containerPort),
        //     'Allow inbound traffic from ALB'
        // );

        // // Create ALB
        // const alb = new elbv2.ApplicationLoadBalancer(this, 'GCLoadBalancer', {
        //     vpc,
        //     internetFacing: true,
        //     securityGroup: lbSecurityGroup,
        // });

        // // Create Target Group
        // const targetGroup = new elbv2.ApplicationTargetGroup(this, 'GCTargetGroup', {
        //     vpc,
        //     port: containerPort,
        //     protocol: elbv2.ApplicationProtocol.HTTP,
        //     targetType: elbv2.TargetType.IP,
        //     healthCheck: {
        //         path: '/actuator/health',
        //     },
        // });

        // // Add Listener
        // const listener = alb.addListener('GCListener', {
        //     port: 80,
        //     defaultTargetGroups: [targetGroup],
        // });

        // // Create Fargate Service
        // const fargateService = new ecs.FargateService(this, 'GCService', {
        //     cluster,
        //     taskDefinition,
        //     serviceName: gcServiceName,
        //     desiredCount: 1,
        //     securityGroups: [containerSecurityGroup],
        //     assignPublicIp: false,
        //     healthCheckGracePeriod: Duration.seconds(60),
        // });

        // fargateService.attachToApplicationTargetGroup(targetGroup);

        // Create a DynamoDB table to store game characters' specifications
        const charactersTable = new dynamodb.Table(this, 'DNDCharactersTable', {
            tableName: `${this._appResourcePrefix}-game-characters`,
            partitionKey: { name: 'character_id', type: dynamodb.AttributeType.STRING },
            removalPolicy: RemovalPolicy.DESTROY,
            billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
        });

        // Outputs
        // new CfnOutput(this, 'GCLoadBalancerDNS', {
        //     value: alb.loadBalancerDnsName,
        //     exportName: 'GCLoadBalancerDNS',
        // });
        new CfnOutput(this, 'DNDCharactersTableName', {
            value: charactersTable.tableName,
            exportName: 'DNDCharactersTableName',
        });


    }

    /**
    * Creates an Amazon Bedrock AgentActionGroup resource.
    *
    * @param kbId - The ID of the Amazon Bedrock knowledge base to use.
    * @returns An Amazon Bedrock AgentActionGroup resource.
    */
    // private createBedrockAgentActionGroup(kbId: string): bedrock.AgentActionGroup {
    //     const actionGroupProps: LambdaProps = {
    //         functionName: `${this._appResourcePrefix}-gc-action-group`,
    //         runtime: lambda.Runtime.NODEJS_20_X,
    //         memorySize: 1024,
    //         entry: join(
    //             __dirname,
    //             `../src/actions-group/${this._llmFramework}-agent-deepf1.ts`
    //         ),
    //         handler: `${this._llmFramework}Handler`,
    //         timeout: Duration.seconds(60),
    //         architecture: lambda.Architecture.ARM_64,
    //         tracing: lambda.Tracing.ACTIVE,
    //         bundling: {
    //             minify: true,
    //             nodeModules: ['@llamaindex/env', 'pgvector', 'pg'],
    //         },
    //         environment: {
    //             KNOWLEDGE_BASE_ID: kbId,
    //             BEDROCK_MODEL_ID: this._llm,
    //             PROMPT_TEMPLATE: this._agentInstruction,
    //             ...lambdaConfig,
    //         },
    //     };
    //     const actionGroupLambda: NodejsFunction = this.createNodeJSLambdaFn(actionGroupProps);
    //     actionGroupLambda.addToRolePolicy(new iam.PolicyStatement({
    //         actions: [
    //             'bedrock:Retrieve',
    //             'bedrock:InvokeModel',
    //         ],
    //         resources: [
    //             `arn:aws:bedrock:${this.region}:${this.account}:knowledge-base/${kbId}`,
    //             `arn:aws:bedrock:${this.region}::foundation-model/${this._llm}`
    //         ],
    //     }));

    //     return new bedrock.AgentActionGroup(this, 'GenAIAgentActionGroup', {
    //         actionGroupName: `${this._appResourcePrefix}-query-kb`,
    //         actionGroupExecutor: {
    //             lambda: actionGroupLambda
    //         },
    //         actionGroupState: "ENABLED",
    //         apiSchema: bedrock.ApiSchema.fromAsset(join(__dirname, '../resources/deepf1-openapi-actions-group.yaml')),
    //     });
    // }

    // private createNodeJSLambdaFn(lambdaProps: LambdaProps): NodejsFunction {
    //     return new NodejsFunction(this, lambdaProps.functionName.replace('-', '').toUpperCase(), lambdaProps);
    // }
}