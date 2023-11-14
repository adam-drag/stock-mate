#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lib.event_emitter_stack import EventEmitterStack
from lib.rds_stack import RdsStack
from lib.vpc_stack import RdsVpcStack

account = os.environ.get("CDK_DEFAULT_ACCOUNT", "707774792834")
region = os.environ.get("CDK_DEFAULT_REGION", "ap-southeast-2")

app = cdk.App()
vpc_stack = RdsVpcStack(app, "RdsVpcStack")
rds_stack = RdsStack(app, vpc_stack, "RdsStack")
EventEmitterStack(app, vpc_stack, rds_stack, "EventEmitterStack")
# MainStack(app, "MainStack", env=Environment(account=account, region=region))

app.synth()
