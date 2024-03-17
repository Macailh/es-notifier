from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import custom_resources as crs
from constructs import Construct


class EsNotifierStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        es_notifier_api_function = _lambda.Function(
            self,
            "EsNotifierApiFunction",
            function_name="esNotifierApiFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_handler.main",
            code=_lambda.Code.from_asset("es_notifier/es_notifier_api_function"),
        )

        es_notifier_api_gateway = apigateway.LambdaRestApi(
            self,
            "EsNotifierApiGateway",
            rest_api_name="esNotifierApiGateway",
            handler=es_notifier_api_function,
        )

        # es_notifier_api_function.add_environment("API_URL", es_notifier_api_gateway.url)
        # Create a CloudFormation Custom Resource to update the Lambda function after creation
        api_url_updater = crs.AwsCustomResource(
            self,
            "APIURLUpdater",
            policy=crs.AwsCustomResourcePolicy.from_sdk_calls(
                resources=crs.AwsCustomResourcePolicy.ANY_RESOURCE
            ),
            on_create=crs.AwsSdkCall(
                action="updateFunctionConfiguration",
                service="Lambda",
                parameters={
                    "FunctionName": es_notifier_api_function.function_name,
                    "Environment": {
                        "Variables": {"API_URL": es_notifier_api_gateway.url}
                    },
                },
                physical_resource_id=crs.PhysicalResourceId.of(
                    es_notifier_api_function.function_name
                ),
            ),
        )

        # Set an explicit dependency to ensure that the API Gateway is created before updating the Lambda function
        api_url_updater.node.add_dependency(es_notifier_api_gateway)
