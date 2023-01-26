"""
Demonstration dag to run DBT jobs via KubernetesPodOperator.

1) Send request to wikipedia, and write data to S3
2) Execute DBT job

"""

import os
from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from operators.SimpleRequestAndWriteOperator import SimpleRequestAndWriteOperator
from utils.common import generate_k8s_secrets
from utils.constants import DBT_PROFILES_PARAM_NAMES, ASSETS_DIR

DAG_NAME = "dbt_snowflake_demo"
DBT_ASSETS = os.path.join(ASSETS_DIR, DAG_NAME)

dag = DAG(
    dag_id=DAG_NAME,
    start_date=datetime(2021, 11, 17),
    schedule_interval="45 0 * * *",
    catchup=False,
    max_active_runs=1,
    max_active_tasks=1,
)
dag.doc_md = __doc__


request_to_s3 = SimpleRequestAndWriteOperator(
    url="https://www.wikipedia.org/",
    s3_conn_id="s3_conn_id",
    s3_bucket="data",
    filename="status.txt",
    task_id="request_to_s3",
    dag=dag,
)

# There are multiple approaches to move data in s3 to snowflake
# I prefer the use of external tables which can then be queried as part of dbt run.

run_model = KubernetesPodOperator(
    namespace="airflow",
    image="localhost:5000/dbt-snowflake:latest",
    env_vars=generate_k8s_secrets(DBT_PROFILES_PARAM_NAMES),
    cmds=["dbt"],
    arguments=["run", "--select", "test", "--full-refresh"],
    name="dbt-pod",
    is_delete_operator_pod=True,
    in_cluster=True,
    task_id="run_model",
    get_logs=True,
    image_pull_policy="IfNotPresent",
    dag=dag,
)

request_to_s3 >> run_model
