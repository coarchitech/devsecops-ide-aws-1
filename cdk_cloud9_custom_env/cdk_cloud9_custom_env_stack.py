import os

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import (core as cdk,
                     aws_cloud9 as cloud9,
                     aws_ec2 as ec2,
                     aws_lambda as _lambda,
                     aws_iam as iam,
                     aws_codecommit as codecommit)


class CdkCloud9CustomEnvStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, props: dict = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        dirname = os.path.dirname(__file__)

        # The code that defines your stack goes here
        # vpc_id = core.CfnParameter(self, "VPCID", description="VPCID for cloud9 instance", type='string',
        #                          allowed_pattern="^[0-9a-zA-Z]+([0-9a-zA-Z-]*[0-9a-zA-Z])*$")
        vpc_id = props['vpc_id']

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)
        # create a cloud9 ec2 environment in import VPC
        # import Repositories
        repos = []

        if len(props["codecommit_repos"]) > 0:

            for r in props["codecommit_repos"]:
                repos.append(
                    cloud9.CloneRepository.from_code_commit(
                        repository=codecommit.Repository.from_repository_name(self, f"Repo-{r}", repository_name=r),
                        path= r)

                )

        c9env = cloud9.Ec2Environment(self, "Cloud9Env2",
                                      vpc=vpc,
                                      instance_type=ec2.InstanceType(props['instance_size']),
                                      ec2_environment_name=props['environment_Name'],

                                      description=props['description'],
                                      subnet_selection=ec2.SubnetSelection(subnets=[
                                          ec2.Subnet.from_subnet_id(self, "Sub1",
                                                                    subnet_id=props['subnet_selection'][0]),
                                          ec2.Subnet.from_subnet_id(self, "Sub2",
                                                                    subnet_id=props['subnet_selection'][1])]),
                                      cloned_repositories=repos

                                      )


        c9_role = iam.Role(self, "Cloud9InstanceRole", role_name=f"Cloud9InstanceRole-{props['environment_Name']}",
                           assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                           managed_policies=[
                               iam.ManagedPolicy.from_managed_policy_arn(self,
                                                                         id="AdminPol",
                                                                         managed_policy_arn="arn:aws:iam::aws:policy/AdministratorAccess")
                               #"arn:aws:iam::aws:policy/AWSCloud9SSMInstanceProfile")
                           ]

                           )
        c9_instance_profile = iam.CfnInstanceProfile(self, "Cloud9InstanceProfile",
                                                     instance_profile_name=f"Cloud9InstanceProfile-{props['environment_Name']}",
                                                     roles=[c9_role.role_name])

        # Create policies for lambda Role
        st = iam.PolicyStatement(actions=[
            "cloudformation:DescribeStackResources",
            "ec2:AssociateIamInstanceProfile",
            "ec2:AuthorizeSecurityGroupIngress",
            "ec2:DescribeInstances",
            "ec2:DescribeInstanceStatus",
            "ec2:DescribeInstanceAttribute",
            "ec2:DescribeIamInstanceProfileAssociations",
            "ec2:DescribeVolumes",
            "ec2:DesctibeVolumeAttribute",
            "ec2:DescribeVolumesModifications",
            "ec2:DescribeVolumeStatus",
            "ec2:StartInstances",
            "ec2:StopInstances",
            "ssm:DescribeInstanceInformation",
            "ec2:ModifyVolume",
            "ec2:ReplaceIamInstanceProfileAssociation",
            "ec2:ReportInstanceStatus",
            "ssm:SendCommand",
            "ssm:GetCommandInvocation",
            "s3:GetObject"
        ],
            resources=["*"],
            effect=iam.Effect.ALLOW)
        st2 = iam.PolicyStatement(actions=["iam:PassRole"],
                                  resources=[c9_role.role_arn],
                                  effect=iam.Effect.ALLOW)
        st3 = iam.PolicyStatement(actions=['lambda:AddPermission',
                                           'lambda:RemovePermission'],
                                  resources=['*'],
                                  effect=iam.Effect.ALLOW)
        st4 = iam.PolicyStatement(actions=[
            'events:PutRule',
            'events:DeleteRule',
            'events:PutTargets',
            'events:RemoveTargets',
        ],
            resources=['*'], effect=iam.Effect.ALLOW)

        lambda_role = iam.Role(self, "LambdaCloud9Role", role_name=f"LambdaCloud9Role-{props['environment_Name']}",
                               assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),

                               )
        lambda_role.add_to_policy(st)
        lambda_role.add_to_policy(st2)
        lambda_role.add_to_policy(st3)
        lambda_role.add_to_policy(st4)
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(self,
                                                                         id="lambdaPol",
                                                                         managed_policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"))
        # arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

        # Create lambda to setup Role
        setup_role = _lambda.Function(self, f'C9SetupRoleLambda',
                                      runtime=_lambda.Runtime.PYTHON_3_8,
                                      code=_lambda.Code.asset(
                                          os.path.join(dirname, "set_custom_role_c9/C9_setup_role/function")),
                                      handler='lambda_function.handler',
                                      function_name=f"C9InstanceProfileLambda-{props['environment_Name']}",
                                      timeout=core.Duration.seconds(900),
                                      role=lambda_role
                                      )

        c1 = cdk.CustomResource(self, f"Setup-Role-{props['environment_Name']}",
                                service_token=setup_role.function_arn,
                                properties=dict(Cloud9Environment=c9env.environment_id,
                                                InstanceProfile=c9_instance_profile.instance_profile_name))

        # Create resize Disk Function
        resize_disk = _lambda.Function(self, f'ResizeDiskLambda',
                                       runtime=_lambda.Runtime.PYTHON_3_8,
                                       code=_lambda.Code.asset(
                                           os.path.join(dirname, "resize_disk_function/resize_disk/function")),
                                       handler='lambda_function.handler',
                                       function_name=f"ResizeDiskLambda-{props['environment_Name']}",
                                       timeout=core.Duration.seconds(900),
                                       role=lambda_role
                                       )

        cdk.CustomResource(self, f"Resize-Disk-{props['environment_Name']}",
                           service_token=resize_disk.function_arn,
                           properties=dict(EBSVolumeSize=props["EBS_Volumesize"],
                                           InstanceId=c1.ref,
                                           Region=cdk.Aws.REGION
                                           ),
                           )

        # Bootstraping Function
        boots_env = _lambda.Function(self, f"BootStrapEnv-{props['environment_Name']}",
                                     runtime=_lambda.Runtime.PYTHON_3_8,
                                     code=_lambda.Code.asset(
                                         os.path.join(dirname, "bootstrap_env_function/bootstrap_env/function")),
                                     handler='lambda_function.handler',
                                     function_name=f"BootStrapEnv-{props['environment_Name']}",
                                     timeout=core.Duration.seconds(900),
                                     role=lambda_role
                                     )

        cdk.CustomResource(self, f"Bootstrap-{props['environment_Name']}", service_token=boots_env.function_arn,
                           properties=dict(InstanceId=c1.ref,
                                           BootstrapArguments=props["bootstrap_commands"],
                                           ),
                           )

        # print the Cloud9 IDE URL in the output
        cdk.CfnOutput(self, "URL", value=c9env.ide_url)


