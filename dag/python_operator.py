# https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html
from pprint import pprint

from airflow.operators.python import PythonOperator, BranchPythonOperator

from dag import *

dag = makeDag("python_operator")

# use template dictionary, operator argument on parameter
def print_context(a, ds, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    pprint(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'


run_this = PythonOperator(
    task_id='print_the_context',
    python_callable=print_context,
    op_kwargs={'a': 1},
    dag=dag,
)

BranchPythonOperator