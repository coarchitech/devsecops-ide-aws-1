#!/usr/bin/env python3

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from cdk_cloud9_custom_env.cdk_cloud9_custom_env_stack import CdkCloud9CustomEnvStack
from project_configurations import project_props


app = core.App()
env = core.Environment(account=project_props.account, region=project_props.region)


c9 = CdkCloud9CustomEnvStack(app, f"c9-{project_props.props['environment_Name']}", props=project_props.props, env=env
                             # If you don't specify 'env', this stack will be environment-agnostic.
                             # Account/Region-dependent features and context lookups will not work,
                             # but a single synthesized template can be deployed anywhere.

                             # Uncomment the next line to specialize this stack for the AWS Account
                             # and Region that are implied by the current CLI configuration.

                             # env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

                             # Uncomment the next line if you know exactly what Account and Region you
                             # want to deploy the stack to. */

                             # env=core.Environment(account='123456789012', region='us-east-1'),

                             # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                             )
# Add Tags here in props

for t in project_props.props["tags"]:
    core.Tags.of(c9).add(key=t['key'], value=t['value'])

app.synth()
