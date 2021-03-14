from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator, ShortCircuitOperator
from operators.dags import *

dag = makeDag("branch_test")

def should_run(**kwargs):
    """
    Determine which dummy_task should be run based on if the execution date minute is even or odd.

    :param dict kwargs: Context
    :return: Id of the task to run
    :rtype: str
    """
    print(
        '------------- exec dttm = {} and minute = {}'.format(
            kwargs['execution_date'], kwargs['execution_date'].minute
        )
    )
    if kwargs['execution_date'].minute % 2 == 0:
        return "dummy_task_1"
    else:
        return "dummy_task_2"


cond = BranchPythonOperator(
    task_id='condition',
    python_callable=should_run,
    dag=dag,
)

dummy_task_1 = DummyOperator(task_id='dummy_task_1', dag=dag)
dummy_task_2 = DummyOperator(task_id='dummy_task_2', dag=dag)
cond >> [dummy_task_1, dummy_task_2]

# If there is no multiple branch. but only single task. then use this to skip when it's false.
cond_true = ShortCircuitOperator(
    task_id='condition_is_True',
    python_callable=lambda: True,
    dag=dag,
)

ds_true = [DummyOperator(task_id='true_' + str(i), dag=dag) for i in [1, 2]]
# If there is multiple starting task, all of them get started
chain(cond_true, *ds_true)