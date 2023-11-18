from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha,
    Stack, Duration,
    aws_lambda_event_sources as lambda_event_sources,
    aws_sns_subscriptions as sns_subscriptions
)
from constructs import Construct
from lib.sns_stack import SnsStack
from lib.rds_stack import RdsStack
from lib.vpc_stack import RdsVpcStack


class PersistenceStack(Stack):

    def __init__(self, scope: Construct, vpc: RdsVpcStack, rds_stack: RdsStack, sns_stack: SnsStack, id: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

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

        persistence_role = iam.Role(
            self, "PersistencerRole",
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

        persistence_lambda = aws_lambda_python_alpha.PythonFunction(
            self, "PersistenceLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            entry="../persistence-service",
            index="app.py",
            handler="lambda_handler",
            role=persistence_role,
            environment={
                "NEW_PRODUCT_PERSISTED_SNS_ARN": sns_stack.product_persisted_topic.topic_arn,
                "NEW_SUPPLIER_PERSISTED_SNS_ARN": sns_stack.supplier_persisted_topic.topic_arn,
                "NEW_PURCHASE_ORDER_PERSISTED_SNS_ARN": sns_stack.purchase_order_persisted_topic.topic_arn,
                "NEW_DELIVERY_PERSISTED_SNS_ARN": sns_stack.delivery_persisted_topic.topic_arn,
                "DB_HOST": rds_stack.db_instance.db_instance_endpoint_address,
                "DB_PORT": rds_stack.db_instance.db_instance_endpoint_port,
                "DB_SECRET_NAME": rds_stack.db_secret.secret_name,
                "DB_NAME": rds_stack.db_name,
            },
            security_groups=[vpc.lambda_security_group],
            vpc=vpc.custom_vpc,
            timeout=Duration.seconds(30),
        )

        sns_stack.product_scheduled_topic.add_subscription(
            sns_subscriptions.LambdaSubscription(persistence_lambda)
        )

        sns_stack.supplier_scheduled_topic.add_subscription(
            sns_subscriptions.LambdaSubscription(persistence_lambda)
        )

        sns_stack.purchase_order_scheduled_topic.add_subscription(
            sns_subscriptions.LambdaSubscription(persistence_lambda)
        )

        sns_stack.delivery_scheduled_topic.add_subscription(
            sns_subscriptions.LambdaSubscription(persistence_lambda)
        )
