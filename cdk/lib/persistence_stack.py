from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_lambda_python_alpha,
    Stack,
)
from constructs import Construct

from rds_stack import RdsStack
from vpc_stack import RdsVpcStack


class PersistenceStack(Stack):
    def __init__(self, scope: Construct, vpc: RdsVpcStack, rds_stack: RdsStack, id: str, **kwargs) -> None:
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
        persistence_service_role = iam.Role(
            self, "PersistenceServiceLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ],
            inline_policies={"RDS_Data_CRUD_Policy": rds_data_crud_policy},
        )
        persistence_service_lambda = aws_lambda_python_alpha.PythonFunction(
            self, "PersistenceServiceLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            entry="../persistence-service",
            index="app.py",
            handler="lambda_handler",
            role=persistence_service_role,
            vpc=vpc.custom_vpc,
            security_groups=[vpc.egress_security_group, vpc.ingress_security_group],
            environment={
                "DB_HOST": rds_stack.db_instance.db_instance_endpoint_address,
                "DB_PORT": rds_stack.db_instance.db_instance_endpoint_port,
                "DB_SECRET_NAME": rds_stack.db_secret.secret_name,
                "DB_NAME": rds_stack.db_name,
            }
        )
