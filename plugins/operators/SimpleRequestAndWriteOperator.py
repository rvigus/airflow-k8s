import os
from datetime import datetime
import requests
import tempfile
from airflow.models import BaseOperator, Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


class SimpleRequestAndWriteOperator(BaseOperator):
    def __init__(
        self,
        url,
        s3_conn_id,
        s3_bucket,
        filename,
        s3_prefix=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.url = url
        self.s3_conn_id = s3_conn_id
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
        self.filename = filename

    def make_request(self, url):
        """
        Sends a request and returns status code.

        """
        r = requests.get(url)
        return r.status_code

    def execute(self, context):
        """
        Run
        """

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log.info(f"Making request to {self.url}")
        status = self.make_request(url=self.url)

        self.log.info("Writing file to S3")

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(bytes(status))
            temp_file_name = temp.name

            s3 = S3Hook(aws_conn_id=self.s3_conn_id)
            if not self.s3_prefix:
                self.s3_prefix = ""
            s3_key = os.path.join(self.s3_prefix, f"{timestamp}_{self.filename}")

            s3.load_file(
                filename=temp_file_name,
                key=s3_key,
                bucket_name=self.s3_bucket,
                replace=True,
            )
            self.log.info(f"File written to {os.path.join(self.s3_bucket, s3_key)}")
