from datetime import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator


dag = DAG(
    dag_id="dbt_snowflake_test",
    start_date=datetime(2021, 11, 17),
    schedule_interval="45 0 * * *",
    catchup=False,
    max_active_runs=1,
    max_active_tasks=1,
)

test_run = KubernetesPodOperator(
    namespace="airflow",
    image="localhost:5000/dbt-snowflake",
    cmds=["dbt"],
    arguments=["run", "--select", "test", "--full-refresh"],
    name="dbt-pod",
    is_delete_operator_pod=True,
    in_cluster=True,
    task_id="test_run",
    get_logs=True,
    image_pull_policy="IfNotPresent",
    dag=dag
)


