# https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from dag import *

dag = makeDag("bash_operator")

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)

# https://jinja.palletsprojects.com/
templated_command = """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
    echo "{{ params.my_param }}"
{% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag,
)

# set bash environment variable
# recommended to use for accessing configuration.
t4 = BashOperator(
    task_id="bash_task",
    bash_command='echo "here is the message: \'$message\'"',
    env={'message': '{{ dag_run.conf["message"] if dag_run else "" }}'},
)

# use script file : https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html#troubleshooting
t5 = BashOperator(
    task_id='bash_example',

    # when using Jinja template
    # bash_command="/home/batcher/test.sh",

    # without template(need space in the end)
    bash_command="/home/batcher/test.sh ",
    dag=dag)
