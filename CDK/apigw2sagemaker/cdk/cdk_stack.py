from aws_cdk import (
    # Duration,
    CfnParameter,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
    aws_iam as _iam
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # RestApiName  = CfnParameter(self, 'RestApiName', 
        #                                 type="String",
        #                                 description="The name of the restful API.")
        # RestApiName = self.node.try_get_context('RestApiName')
        #RestApiName = RestApiName.value_as_string
        RestApiName = "apigw2sm"

        SageMakerEndpointName  = CfnParameter(self, 'SageMakerEndpointName', 
                                        type="String",
                                        description="The name of the Amazon SageMaker Endpoint.")
        SageMakerEndpointName = self.node.try_get_context('SageMakerEndpointName')
        #SageMakerEndpointName = SageMakerEndpointName.value_as_string

        # The code that defines your stack goes here
        # create a SageMaker Invoke Role
        base_policy = _iam.Policy(self, RestApiName + "-Policy",
                                statements=[_iam.PolicyStatement(
                                    effect=_iam.Effect.ALLOW,
                                    actions=["sagemaker:InvokeEndpoint"],
                                    resources=["*"]
                                )])

        # create a lambda function
        base_lambda = _lambda.Function(self, RestApiName + "-Lambda",
                                       handler='lambda-handler.handler',
                                       runtime=_lambda.Runtime.PYTHON_3_9,
                                       environment={
                                           "ENDPOINT_NAME": SageMakerEndpointName,
                                       },
                                       code=_lambda.Code.from_asset('lambda'))
        base_lambda.role.attach_inline_policy(base_policy)

        # create a api gateway
        base_api = _apigw.RestApi(self, RestApiName + "-GW")
        
        integrationResponses = [_apigw.IntegrationResponse(
            status_code="200",
        )]

        integrateion = _apigw.LambdaIntegration(handler=base_lambda, 
                                                proxy=False,
                                                integration_responses = integrationResponses)
        methodResponses = [_apigw.MethodResponse(
            status_code="200",
        )]

        items = base_api.root.add_resource("items")
        items.add_method("POST", integrateion, method_responses=methodResponses) # POST /items

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

