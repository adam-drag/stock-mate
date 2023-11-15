from aws_cdk import (
    aws_iam as iam,
    aws_sns as sns,
    aws_lambda as _lambda,
    aws_lambda_python_alpha,
    aws_apigateway as apigateway,
    Stack, Duration,
)
from constructs import Construct
from lib.sns_stack import SnsStack
from lib.rds_stack import RdsStack
from lib.vpc_stack import RdsVpcStack


class EventEmitterStack(Stack):

    def __init__(self, scope: Construct, vpc: RdsVpcStack, rds_stack: RdsStack, sns_stack: SnsStack, id: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api = apigateway.RestApi(
            self, "APIGateway-event-emitter",
            rest_api_name="APIGateway-event-emitter",
            description="API Gateway for Event Emitter",
        )

        # TODO Consider extracting as its used across lambdas
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
                    resources=[rds_stack.db_instance.instance_arn],
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

        event_emitter_role = iam.Role(
            self, "EventEmitterRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess")
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
                                f"arn:aws:secretsmanager:{self.region}:{self.account}:secret:{rds_stack.db_secret.secret_name}*"],
                        )
                    ],
                ),
            },
        )

        event_emitter_lambda = aws_lambda_python_alpha.PythonFunction(
            self, "EventEmitterLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            entry="../event-emitter-api",
            index="app.py",
            handler="lambda_handler",
            role=event_emitter_role,
            environment={
                "NEW_PRODUCT_SCHEDULED_SNS_ARN": sns_stack.product_scheduled_topic.topic_arn,
                "DB_HOST": rds_stack.db_instance.db_instance_endpoint_address,
                "DB_PORT": rds_stack.db_instance.db_instance_endpoint_port,
                "DB_SECRET_NAME": rds_stack.db_secret.secret_name,
                "DB_NAME": rds_stack.db_name,
            },
            security_groups=[vpc.lambda_security_group],
            vpc=vpc.custom_vpc,
            timeout=Duration.seconds(30),
        )

        event_emitter_api_integration = apigateway.LambdaIntegration(event_emitter_lambda)
        product_resource = self.api.root.add_resource("product")
        product_resource.add_method("POST", event_emitter_api_integration)
