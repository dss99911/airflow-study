from airflow.models import Variable
from airflow.providers.slack.operators.slack import SlackAPIPostOperator


def slack_failed_notification(context):
    """
    Define the callback to post on Slack if a failure is detected in the Workflow
    set on 'on_failure_callback'
    """
    operator = SlackAPIPostOperator(
        task_id='slack_failed_notification',
        text=str(context['task_instance']) + '\n' + 'exception: ' + str(context['exception']),
        token=Variable.get("slack_access_token"),
        channel='#channel_name'
    )
    return operator.execute(context=context)
    # return [operator.execute(context=context), operator.execute(context=context)] #multiple slack operator
