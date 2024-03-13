import aws_cdk as core
import aws_cdk.assertions as assertions

from es_notifier.es_notifier_stack import EsNotifierStack

# example tests. To run these tests, uncomment this file along with the example
# resource in es_notifier/es_notifier_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EsNotifierStack(app, "es-notifier")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
