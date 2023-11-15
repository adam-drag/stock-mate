from aws_cdk import (
    aws_ec2 as ec2,
    Stack,
)
from constructs import Construct


class RdsVpcStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.custom_vpc = ec2.Vpc(
            self, 'RDS_VPC',
            cidr='10.0.0.0/16',
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    cidr_mask=26,
                    name='isolatedSubnet',
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                ),
                ec2.SubnetConfiguration(
                    cidr_mask=26,
                    name='publicSubnet',
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
        )

        self.lambda_security_group = ec2.SecurityGroup(
            self, 'LambdaSecurityGroup',
            vpc=self.custom_vpc,
            allow_all_outbound=True,
            security_group_name='LambdaSecurityGroup',
        )
        self.lambda_security_group.add_ingress_rule(peer=ec2.Peer.ipv4('0.0.0.0/0'), connection=ec2.Port.tcp(80))

        self.ingress_security_group = ec2.SecurityGroup(
                self, 'IngressSecurityGroup',
                vpc=self.custom_vpc,
                allow_all_outbound=False,
                security_group_name='IngressSecurityGroup',
            )
        self.ingress_security_group.add_ingress_rule(peer=ec2.Peer.ipv4('10.0.0.0/16'), connection=ec2.Port.tcp(5432))

        self.egress_security_group = ec2.SecurityGroup(
            self, 'EgressSecurityGroup',
            vpc=self.custom_vpc,
            allow_all_outbound=False,
            security_group_name='EgressSecurityGroup',
        )
        self.egress_security_group.add_egress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(80))

        self.custom_vpc.add_interface_endpoint(
            'SecretsManagerEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
            private_dns_enabled=True,
            security_groups=[self.lambda_security_group],
        )

        self.custom_vpc.add_interface_endpoint(
            'SnsEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService.SNS,
            private_dns_enabled=True,
            security_groups=[self.lambda_security_group],
        )
