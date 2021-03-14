from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from dags import *

# trigger other dag
with makeDag("trigger_dag_operator") as dag:
    trigger = TriggerDagRunOperator(
        task_id="test_trigger_dagrun",
        trigger_dag_id="example_trigger_target_dag",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"message": "Hello World"},  # dag_run config
    )
