from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha,
    aws_ec2 as ec2,
    Stack,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager, Duration, )
from constructs import Construct

from lib.vpc_stack import RdsVpcStack


class RdsStack(Stack):
    def __init__(self, scope: Construct, vpc: RdsVpcStack, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.db_name = "stock_mate_main_db"
        self.db_secret = secretsmanager.Secret(
            self, "DBSecret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username":"dbmaster"}',
                generate_string_key="password",
                exclude_characters="\"@/\\"  # Add any characters you want to exclude
            )
        )
        self.db_instance = rds.DatabaseInstance(
            self, "StockMateRdsInstance",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.of("12", "12.4")
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),

            credentials=rds.Credentials.from_secret(self.db_secret),
            multi_az=False,
            allocated_storage=20,
            max_allocated_storage=100,
            vpc=vpc.custom_vpc,
            security_groups=[vpc.egress_security_group, vpc.ingress_security_group],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
        )
        rds_data_crud_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "rds-data:BatchExecuteStatement",
                        "rds-data:BeginTransaction",
                        "rds-data:CommitTransaction",
                        "rds-data:ExecuteSql",
                        "rds-data:RollbackTransaction",
                    ],
                    resources=[self.db_instance.instance_arn],
                ),
            ],
        )

        ni_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "ec2:CreateNetworkInterface",
                        "ec2:DescribeNetworkInterfaces",
                        "ec2:DeleteNetworkInterface"
                    ],
                    resources=["*"],
                ),
            ],
        )

        logs_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                    ],
                    resources=["*"],
                ),
            ],
        )

        db_initializer_lambda_role = iam.Role(
            self, "DbInitializerRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ],
            inline_policies={
                "RDS_Data_CRUD_Policy": rds_data_crud_policy,
                "NI_policy": ni_policy,
                "logs_policy": logs_policy,
                "SecretsManagerPolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=["secretsmanager:GetSecretValue"],
                            resources=[
                                f"arn:aws:secretsmanager:{self.region}:{self.account}:secret:{self.db_secret.secret_name}*"],
                        )
                    ],
                ),
            },
        )

        db_initializer_lambda = aws_lambda_python_alpha.PythonFunction(
            self, "DbInitializer",
            runtime=_lambda.Runtime.PYTHON_3_9,
            entry="../db_initializer",
            index="app.py",
            handler="lambda_handler",
            vpc=vpc.custom_vpc,
            role=db_initializer_lambda_role,
            environment={
                "DB_HOST": self.db_instance.db_instance_endpoint_address,
                "DB_PORT": self.db_instance.db_instance_endpoint_port,
                "DB_SECRET_NAME": self.db_secret.secret_name,
                "DB_NAME": self.db_name,
            },
            timeout=Duration.minutes(5),
        )
