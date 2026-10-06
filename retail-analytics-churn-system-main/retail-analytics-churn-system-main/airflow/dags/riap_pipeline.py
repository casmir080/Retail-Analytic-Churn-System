from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "riap",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    "riap_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command="cd /opt/airflow && python -m backend.ingestion.generate_data"
    )

    validate = BashOperator(
        task_id="validate_data",
        bash_command="cd /opt/airflow && python -m backend.validation.schema_validator"
    )

    create_tables = BashOperator(
        task_id="create_tables",
        bash_command="cd /opt/airflow && python -m backend.db.create_tables"
    )

    load = BashOperator(
        task_id="load_data",
        bash_command="cd /opt/airflow && python -m backend.ingestion.load_to_postgres"
    )

    transform = BashOperator(
        task_id="build_features",
        bash_command="cd /opt/airflow && python -m backend.transformation.build_features"
    )

    rfm = BashOperator(
        task_id="rfm_features",
        bash_command="cd /opt/airflow && python -m backend.features.rfm"
    )

    train = BashOperator(
        task_id="train_model",
        bash_command="cd /opt/airflow && python -m backend.ml.train"
    )

    trigger = BashOperator(
        task_id="trigger_actions",
        bash_command="cd /opt/airflow && python -m backend.automation.triggers"
    )

    generate_data >> validate >> create_tables >> load >> transform >> rfm >> train >> trigger