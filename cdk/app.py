#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Environment

from lib.main_stack import MainStack

account = os.environ.get("CDK_DEFAULT_ACCOUNT", "707774792834")
region = os.environ.get("CDK_DEFAULT_REGION", "ap-southeast-2")

app = cdk.App()

MainStack(app, "MainStack", env=Environment(account=account, region=region))

app.synth()
