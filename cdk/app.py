#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lib.sns_stack import SnsStack
from lib.event_emitter_stack import EventEmitterStack
from lib.persistence_stack import PersistenceStack
from lib.rds_stack import RdsStack
from lib.vpc_stack import RdsVpcStack

account = os.environ.get("CDK_DEFAULT_ACCOUNT", "707774792834")
region = os.environ.get("CDK_DEFAULT_REGION", "ap-southeast-2")

app = cdk.App()

vpc_stack = RdsVpcStack(app, "RdsVpcStack")
sns_stack = SnsStack(app, "SnsStack")

rds_stack = RdsStack(app, vpc_stack, "RdsStack")

EventEmitterStack(app, vpc_stack, rds_stack, sns_stack, "EventEmitterStack")
PersistenceStack(app, vpc_stack, rds_stack, sns_stack, "PersistenceStack")

app.synth()
