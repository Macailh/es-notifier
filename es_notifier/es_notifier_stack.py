from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class EsNotifierStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        es_notifier_api_function = _lambda.Function(
            self,
            "EsNotifierApiFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_handler.main",
            code=_lambda.Code.from_asset("es_notifier/es_notifier_api_function"),
        )
