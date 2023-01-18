FROM apache/airflow:2.4.1

ARG AIRFLOW_HOME=/opt/airflow/dags

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD dags $AIRFLOW_HOME
ADD plugins $AIRFLOW_HOME
ADD assets $AIRFLOW_HOME
