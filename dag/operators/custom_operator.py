import requests
from airflow.exceptions import AirflowSkipException

from airflow.models.baseoperator import BaseOperator
from airflow.operators.dummy import DummyOperator

DEFAULT_ARGS = {"owner": "airflow"}


class GetRequestOperator(BaseOperator):
    """Custom operator to send GET request to provided url"""

    def __init__(self, *, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = url

    def execute(self, context):
        return requests.get(self.url).json()


def make_get_request_operator():
    GetRequestOperator(task_id='get_ip', url="http://httpbin.org/get")

# able to Skip with AirflowSkipException
class DummySkipOperator(DummyOperator):
    """Dummy operator which always skips the task."""

    ui_color = '#e8b7e4'

    def execute(self, context):
        raise AirflowSkipException