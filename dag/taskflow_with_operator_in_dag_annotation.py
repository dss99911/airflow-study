from typing import Dict, Any

from operators.custom_operator import *
from operators.email_operator import *
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

DEFAULT_ARGS = {"owner": "airflow"}

@dag(default_args=DEFAULT_ARGS, schedule_interval=None, start_date=days_ago(2), tags=['example'])
def taskflow_with_operator(email: str):#able to change email by dag_run.conf on Trigger DAG
    """
        @task function을 호출한 리턴 값은 task와 동일함.

        * @task에서 operator로 연결시키기.
            리턴값의 파라미터를 operator의 매개변수로 넣으면 연결되는 듯
        * operator에서 @task로 연결시키기
            operator.output을 @task의 파라미터로 입력
    """
    get_ip = GetRequestOperator(task_id='get_ip', url="http://httpbin.org/get")

    @task(multiple_outputs=True)
    def prepare_email(raw_json: Dict[str, Any]) -> Dict[str, str]:
        external_ip = raw_json['origin']
        return {
            'subject': f'Server connected from {external_ip}',
            'body': f'Seems like today your server executing Airflow is connected from IP {external_ip}<br>',
        }

    email_info = prepare_email(get_ip.output)
    make_email_operator(email, email_info)


# on Trigger DAG, dag_run.conf default value is {"email": "dss99911@gmail.com"}
dag = taskflow_with_operator("dss99911@gmail.com")