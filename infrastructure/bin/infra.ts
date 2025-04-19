#!/usr/bin/env node

/***** CDK *****/
import 'source-map-support/register';
import { App } from 'aws-cdk-lib';
/***** END CDK *****/

import { DNDGenAIStack } from '../lib/dnd-genai-stack';

const app = new App();

const stackProps = {
    env: {
        account: process.env.AWS_ACCOUNT_ID as string,
        region: process.env.AWS_REGION as string,
    },
};
const devEnv = process.env.DEV_ENV || "local";
if (devEnv === "local") {
    // TO DO: Local development
}
else {
    new DNDGenAIStack(app, 'DNDGenAIStack', {
        ...stackProps,
        description: "This stack creates required GenAI backend resources to provide great D&D Game Sessions on our AI Role Playing Game application"
    });
}
