"""Example DAG demonstrating the usage of the params arguments in templated arguments."""

import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

dag = DAG(
    "example_passing_params_via_test_command",
    default_args={
        "owner": "airflow",
    },
    schedule_interval='* * * * *',
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=4),
    tags=['example'],
)


def my_py_command(test_mode, params):
    """
    Print out the "foo" param passed in via
    `airflow tasks test example_passing_params_via_test_command run_this <date>
    -t '{"foo":"bar"}'`
    """
    if test_mode:
        print(
            " 'foo' was passed in via test={} command : kwargs[params][foo] \
               = {}".format(
                test_mode, params["foo"]
            )
        )
    # Print out the value of "miff", passed in below via the Python Operator
    print(" 'miff' was passed in via task params = {}".format(params["miff"]))
    return 1


my_templated_command = """
    echo " 'foo was passed in via Airflow CLI Test command with value {{ params.foo }} "
    echo " 'miff was passed in via BashOperator with value {{ params.miff }} "
"""

run_this = PythonOperator(
    task_id='run_this',
    python_callable=my_py_command,
    params={"miff": "agg"},
    dag=dag,
)

also_run_this = BashOperator(
    task_id='also_run_this',
    bash_command=my_templated_command,
    params={"miff": "agg"},
    dag=dag,
)


def print_env_vars(test_mode):
    """
    Print out the "foo" param passed in via
    `airflow tasks test example_passing_params_via_test_command env_var_test_task <date>
    --env-vars '{"foo":"bar"}'`
    """
    if test_mode:
        print("foo={}".format(os.environ.get('foo')))
        print("AIRFLOW_TEST_MODE={}".format(os.environ.get('AIRFLOW_TEST_MODE')))


env_var_test_task = PythonOperator(task_id='env_var_test_task', python_callable=print_env_vars, dag=dag)

run_this >> also_run_this