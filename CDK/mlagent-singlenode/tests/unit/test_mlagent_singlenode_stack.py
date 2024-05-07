import aws_cdk as core
import aws_cdk.assertions as assertions

from mlagent_singlenode.mlagent_singlenode_stack import MlagentSinglenodeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in mlagent_singlenode/mlagent_singlenode_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MlagentSinglenodeStack(app, "mlagent-singlenode")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
