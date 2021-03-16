# https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html
from pprint import pprint

from airflow.operators.python import PythonOperator
from operators.dags import *

dag = makeDag("python_operator_test")


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


def getDagRun(**context):
    """
    Print the payload "message" passed to the DagRun conf attribute.

    :param context: The execution context
    :type context: dict
    """
    print("Remotely received value of {} for key=message".format(context["dag_run"].conf["message"]))


run_this = PythonOperator(
    task_id='run_this',
    python_callable=my_py_command,
    params={"miff": "agg"},
    dag=dag,
)
