
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from datetime import timedelta

from airflow.example_dags.subdags.subdag import subdag
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.subdag import SubDagOperator
from airflow.utils.dates import days_ago

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
from airflow.utils.task_group import TaskGroup

default_args = {
    'owner': 'airflow',

    #과거에 동일 task가 성공 했을 때만 수행하기
    #depends_on_past=True, individual task instances will depend on the success of their previous task instance
    # (that is, previous according to execution_date).
    # Task instances with execution_date==start_date will disregard this dependency
    # because there would be no past task instances created for them.
    'depends_on_past': False,

    #depends_on_past가 true인 경우에만 해당되고, 이전 dag의 동일 task만 성공해도 다음 dag가 수행될 수 있는데, 이걸 true로 놓으면,
    # 다음 dag는 이전 dag의 모든 task가 다 처리된 후에 수행 된다는 얘기인 것 같음.
    # 'wait_for_downstream': True,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

def makeDag(dag_id: str):
    return DAG(
        dag_id,
        default_args=default_args,
        description='A simple tutorial DAG',
        schedule_interval=timedelta(days=1),
        # schedule_interval="@daily",
        # schedule_interval="@once",
        # schedule_interval=None,

        # if set past date, when the DAG's scheduler unpaused, it processes since the past date to now. so, backfill the past date
        # if set 2days ago with days interval, dag is called 2 times for 2days ago, 1days ago.
        start_date=days_ago(2),
        tags=['example'],

        dagrun_timeout=timedelta(minutes=60),
        params={"example_key": "example_value"}
    )


def subDag():
    """
        subDag에 다른 argument를 제공할 때, 사용 하는 듯?
    """
    DAG_NAME = "subdag_test"
    dag = makeDag("subdag_test")
    start = DummyOperator(
        task_id='start',
        dag=dag,
    )

    section_1 = SubDagOperator(
        task_id='section-1',
        subdag=subdag(DAG_NAME, 'section-1', {'owner': 'airflow'}),
        dag=dag,
    )
    start >> section_1

def dagGroup():
    """
        * with DAG를 쓰면, 그 내부에 있는 Operator는 파라미터에 dag를 안 넣어줘도 되는 것 같음.
        * Group을 만들면, 전체 DAG에서  Group으로 테스크 연결하면, 그룹에도 DAG가 있어서, 그룹내의 DAG 생성.
    """
    with DAG(dag_id="example_task_group", start_date=days_ago(2), tags=["example"]) as dag:
        start = DummyOperator(task_id="start")

    # [START howto_task_group_section_1]
    with TaskGroup("section_1", tooltip="Tasks for section_1") as section_1:
        task_1 = DummyOperator(task_id="task_1")
        task_2 = BashOperator(task_id="task_2", bash_command='echo 1')
        task_3 = DummyOperator(task_id="task_3")

        task_1 >> [task_2, task_3]
    # [END howto_task_group_section_1]

    # [START howto_task_group_section_2]
    with TaskGroup("section_2", tooltip="Tasks for section_2") as section_2:
        task_1 = DummyOperator(task_id="task_1")

        # [START howto_task_group_inner_section_2]
        with TaskGroup("inner_section_2", tooltip="Tasks for inner_section2") as inner_section_2:
            task_2 = BashOperator(task_id="task_2", bash_command='echo 1')
            task_3 = DummyOperator(task_id="task_3")
            task_4 = DummyOperator(task_id="task_4")

            [task_2, task_3] >> task_4
        # [END howto_task_group_inner_section_2]

    # [END howto_task_group_section_2]

    end = DummyOperator(task_id='end')

    start >> section_1 >> section_2 >> end