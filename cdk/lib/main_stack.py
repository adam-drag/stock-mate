from aws_cdk import (
    aws_iam as iam,
    aws_sns as sns,
    aws_lambda as _lambda,
    aws_lambda_python_alpha,
    aws_sns_subscriptions as subscriptions,
    aws_apigateway as apigateway,
    aws_ec2 as ec2,
    Stack,
    aws_rds as rds,
    aws_events as events,
    aws_events_targets as targets,
    aws_secretsmanager as secretsmanager, Environment, Duration, )
from constructs import Construct


class MainStack(Stack):
    def __init__(self, scope: Construct, id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)

        # SNS Topic
        product_scheduled_topic = sns.Topic(self, "NewProductScheduled")

        # EventEmitterLambda Role
        event_emitter_role = iam.Role(
            self, "EventEmitterLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess")
            ]
        )

        # API Gateway
        # api_gw_log_group = logs.LogGroup(
        #     self, "APIGatewayLogGroup", retention=logs.RetentionDays.ONE_DAY
        # )

        self.api = apigateway.RestApi(
            self, "APIGateway-event-emitter",
            rest_api_name="APIGateway-event-emitter",
            description="API Gateway for Event Emitter",
            # deploy_options=apigateway.StageOptions(
            # access_log_destination=apigateway.LogGroupLogDestination(api_gw_log_group),
            # access_log_format=apigateway.AccessLogFormat.clf(),
            # data_trace_enabled=True,
            # logging_level=apigateway.MethodLoggingLevel.INFO,
            # metrics_enabled=True,
            # ),
        )

        # VPC and Security Group
        vpc = ec2.Vpc(self, "NewVpc",
                      max_azs=2,
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              name="private",
                              subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                              cidr_mask=24
                          )
                      ])

        shared_security_group = ec2.SecurityGroup(
            self, "LambdaAndRdsSecurityGroup",
            vpc=vpc,
            description="Shared security group for Lambda and RDS",
            allow_all_outbound=True
        )

        # RDS Database
        db_secret = secretsmanager.Secret(
            self, "DBSecret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username":"dbmaster"}',
                generate_string_key="password",
                exclude_characters="\"@/\\"  # Add any characters you want to exclude
            )
        )

        db_instance = rds.DatabaseInstance(
            self, "StockMateRdsInstance",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.of("12", "12.4")
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),

            credentials=rds.Credentials.from_secret(db_secret),
            multi_az=False,
            allocated_storage=20,
            max_allocated_storage=100,
            vpc=vpc,
            security_groups=[shared_security_group],
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
                    resources=[db_instance.instance_arn],
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

        db_name = "stock_mate_main_db"

        persistence_service_lambda = aws_lambda_python_alpha.PythonFunction(
            self, "PersistenceServiceLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            entry="../persistence-service",
            index="app.py",
            handler="lambda_handler",
            role=persistence_service_role,
            environment={
                "DB_HOST": db_instance.db_instance_endpoint_address,
                "DB_PORT": db_instance.db_instance_endpoint_port,
                "DB_SECRET_NAME": db_secret.secret_name,
                "DB_NAME": db_name,
            }
        )

        event_emitter_lambda = aws_lambda_python_alpha.PythonFunction(
            self, "EventEmitterLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            entry="../event-emitter-api",
            index="app.py",
            handler="lambda_handler",
            role=event_emitter_role,
            environment={
                "NEW_PRODUCT_SCHEDULED_SNS_ARN": product_scheduled_topic.topic_arn,
                "DB_HOST": db_instance.db_instance_endpoint_address,
                "DB_PORT": db_instance.db_instance_endpoint_port,
                "DB_SECRET_NAME": db_secret.secret_name,
                "DB_NAME": db_name,
            },
        )

        db_initializer_lambda_role = iam.Role(
            self, "DbInitializerRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ],
            inline_policies={
                "RDS_Data_CRUD_Policy": rds_data_crud_policy,
                "SecretsManagerPolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=["secretsmanager:GetSecretValue"],
                            resources=[
                                f"arn:aws:secretsmanager:{self.region}:{self.account}:secret:{db_secret.secret_name}*"],
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
            vpc=vpc,
            role=db_initializer_lambda_role,
            environment={
                "DB_HOST": db_instance.db_instance_endpoint_address,
                "DB_PORT": db_instance.db_instance_endpoint_port,
                "DB_SECRET_NAME": db_secret.secret_name,
                "DB_NAME": db_name,
            },
            timeout=Duration.minutes(5),
        )

        rule = events.Rule(
            self, "OnRDSInstanceCreation",
            event_pattern={
                "source": ["aws.rds"],
                "detail": {
                    "eventName": ["CreateDBInstance"]
                }
            }
        )

        rule.add_target(targets.LambdaFunction(db_initializer_lambda))

        event_emitter_api_integration = apigateway.LambdaIntegration(event_emitter_lambda)
        product_resource = self.api.root.add_resource("product")
        product_resource.add_method("POST", event_emitter_api_integration)

        persistence_service_lambda.vpc = vpc
        persistence_service_lambda.security_groups = [shared_security_group]

        event_emitter_lambda.vpc = vpc
        event_emitter_lambda.security_groups = [shared_security_group]

        db_initializer_lambda.vpc = vpc
        db_initializer_lambda.security_groups = [shared_security_group]

        product_scheduled_topic.add_subscription(subscriptions.LambdaSubscription(persistence_service_lambda))
