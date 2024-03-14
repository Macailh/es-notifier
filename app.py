#!/usr/bin/env python3
import os

import aws_cdk as cdk

from es_notifier.es_notifier_stack import EsNotifierStack


app = cdk.App()
EsNotifierStack(app, "EsNotifierStack")

app.synth()
