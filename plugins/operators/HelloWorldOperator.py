from airflow.models import BaseOperator


class HelloWorldOperator(BaseOperator):
    """
    Dummy operator

    """

    def __init__(
        self,
        message,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.message = message

    def execute(self, context):
        self.log.info(self.message)
