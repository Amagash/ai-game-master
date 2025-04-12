#!/usr/bin/env node

/***** CDK *****/
import 'source-map-support/register';
import { App } from 'aws-cdk-lib';
/***** END CDK *****/

// import { LocalGenAIStack } from '../lib/local-stack';
import { GenAIDNDStack } from '../lib/genai-dnd-stack';

const app = new App();

const stackProps = {
    env: {
        account: process.env.AWS_ACCOUNT_ID as string,
        region: process.env.AWS_REGION as string,
    },
};
const devEnv = process.env.DEV_ENV || "local";
if (devEnv === "local") {
    // new LocalGenAIStack(app, "LocalGenAIStack", {
    //     ...stackProps,
    //     description: "This stack creates backend resources (locally) to experiment on our AI Role Playing Game application"
    // });
}
else {
    new GenAIDNDStack(app, 'GenAIDNDStack', {
        ...stackProps,
        description: "This stack creates backend resources for our AI Role Playing Game application"
    });
}
