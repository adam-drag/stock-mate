#!/usr/bin/env python3

import aws_cdk as cdk

from lib.main_stack import MainStack

app = cdk.App()

MainStack(app, "MainStack")

app.synth()
