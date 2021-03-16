import datetime as dt

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

"""
옛날 task 는 호출 안되고, 가장 최신 task만 호출됨. backfill이 안된다고 보면 될듯.
task2는 스킵되지 않았는데, task3,4는 스킵됨. latest_only와 연결된 task1,3,4가 모두 스킵되서, task2가 호출되어도 task3,4는 호출 안되는듯
task4의 TriggerRule.ALL_DONE으로 하면, 모든게 다 처리되고, 앞에 것이 스킵 되어도, 수행됨.
"""
dag = DAG(
    dag_id='latest_only_operator_test',
    schedule_interval=dt.timedelta(hours=4),
    start_date=days_ago(2),
    tags=['example3'],
)

latest_only = LatestOnlyOperator(task_id='latest_only', dag=dag)
task1 = DummyOperator(task_id='task1', dag=dag)
task2 = DummyOperator(task_id='task2', dag=dag)
task3 = DummyOperator(task_id='task3', dag=dag)
task4 = DummyOperator(task_id='task4', dag=dag)
# task4 = DummyOperator(task_id='task4', dag=dag, trigger_rule=TriggerRule.ALL_DONE)

latest_only >> task1 >> [task3, task4]
task2 >> [task3, task4]