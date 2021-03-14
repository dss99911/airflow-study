from airflow.operators.dummy import DummyOperator
from airflow.sensors.external_task import ExternalTaskMarker, ExternalTaskSensor
from airflow.sensors.filesystem import FileSensor

from operators.dags import *


def file_sensor():
    file_task = FileSensor(task_id='check_file', filepath='/tmp/order_data.csv')


def task_sensor():
    """
        TODO 샘플 예제 잘 작동 안함..

        DAG가 동일 파일에 두개 있으면, DAG두개 생성됨
        각각의 dag가 다른 dag를 참조 할수 있음
    """
    with makeDag("task_marker_test") as parent_dag:
        parent_task = ExternalTaskMarker(
            task_id="parent_task",
            external_dag_id="task_sensor_test",
            external_task_id="child_task1",
        )

    with makeDag("task_sensor_test") as child_dag:
        child_task1 = ExternalTaskSensor(
            task_id="child_task1",
            external_dag_id=parent_dag.dag_id,
            external_task_id=parent_task.task_id,
            timeout=600,
            allowed_states=['success'],
            failed_states=['failed', 'skipped'],
            mode="reschedule",
        )

        child_task2 = DummyOperator(task_id="child_task2")
        child_task1 >> child_task2
