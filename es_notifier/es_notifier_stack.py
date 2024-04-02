import os
from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import custom_resources as crs
from aws_cdk import aws_iam as iam
from constructs import Construct


class EsNotifierStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        exclude_files = ["__pycache__", "test/", "local.py"]

        es_notifier_api_function_layer = _lambda.LayerVersion(
            self,
            "esNotifierApiFunctionLayer",
            code=_lambda.Code.from_asset("es_notifier/es_notifier_api_function_layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
        )

        es_notifier_api_function_role = iam.Role(
            self,
            "EsNotifierApiFunctionRole",
            role_name="EsNotifierApiFunctionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSESFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
            ],
        )

        es_notifier_api_function = _lambda.Function(
            self,
            "EsNotifierApiFunction",
            function_name="esNotifierApiFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="main.handler",
            code=_lambda.Code.from_asset(
                "es_notifier/es_notifier_api_function", exclude=exclude_files
            ),
            layers=[es_notifier_api_function_layer],
            role=es_notifier_api_function_role,
        )

        es_notifier_api_gateway = apigateway.LambdaRestApi(
            self,
            "EsNotifierApiGateway",
            rest_api_name="esNotifierApiGateway",
            handler=es_notifier_api_function,
            proxy=False,
        )

        root_resource = es_notifier_api_gateway.root
        api_resource = root_resource.add_resource("api")
        v1_resource = api_resource.add_resource("v1")
        proxy_resource = v1_resource.add_proxy(
            any_method=True,
            default_method_options=apigateway.MethodOptions(api_key_required=True),
        )

        docs_resource = root_resource.add_resource("docs")
        docs_resource.add_method("GET")

        openapi_resource = root_resource.add_resource("openapi.json")
        openapi_resource.add_method("GET")

        es_notifier_api_key = apigateway.ApiKey(
            self,
            "EsNotifierApiKey",
            api_key_name="esNotifierApiKey",
            description="API key for esNotifierApi",
        )

        es_notifier_api_usage_plan = apigateway.UsagePlan(
            self,
            "EsNotifierApiUsagePlan",
            name="esNotifierApiUsagePlan",
            api_stages=[
                apigateway.UsagePlanPerApiStage(
                    api=es_notifier_api_gateway,
                    stage=es_notifier_api_gateway.deployment_stage,
                )
            ],
            throttle=apigateway.ThrottleSettings(rate_limit=10, burst_limit=2),
            quota=apigateway.QuotaSettings(limit=1000, period=apigateway.Period.MONTH),
        )

        es_notifier_api_usage_plan.add_api_key(es_notifier_api_key)

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
                        "Variables": {
                            "API_URL": es_notifier_api_gateway.url,
                            "ROOT_PATH": "/"
                            + es_notifier_api_gateway.deployment_stage.stage_name,
                            "SENDER": os.getenv("SENDER", ""),
                        }
                    },
                },
                physical_resource_id=crs.PhysicalResourceId.of(
                    es_notifier_api_function.function_name
                ),
            ),
            on_update=crs.AwsSdkCall(
                action="updateFunctionConfiguration",
                service="Lambda",
                parameters={
                    "FunctionName": es_notifier_api_function.function_name,
                    "Environment": {
                        "Variables": {
                            "API_URL": es_notifier_api_gateway.url,
                            "ROOT_PATH": "/"
                            + es_notifier_api_gateway.deployment_stage.stage_name,
                            "SENDER": os.getenv("SENDER", ""),
                        }
                    },
                },
                physical_resource_id=crs.PhysicalResourceId.of(
                    es_notifier_api_function.function_name
                ),
            ),
        )

        # Set an explicit dependency to ensure that the API Gateway is created before updating the Lambda function
        api_url_updater.node.add_dependency(es_notifier_api_gateway)
