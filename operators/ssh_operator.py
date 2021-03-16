from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.providers.ssh.operators.ssh import SSHOperator


def get_ssh_op(script):
    return SSHOperator(
        task_id=f'ssh_test',
        ssh_hook=SSHHook(ssh_conn_id='ssh_conn'),
        ssh_conn_id='operator_test',
        retries=0,
        command=script)