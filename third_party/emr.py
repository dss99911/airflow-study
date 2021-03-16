# -*- coding: utf-8 -*-

# https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/emr.html

from airflow.providers.amazon.aws.operators.emr_add_steps import EmrAddStepsOperator
from airflow.providers.amazon.aws.sensors.emr_step import EmrStepSensor
from operators.dags import *

DAILY_PARSE_MESSAGE_DAG_ID = 'daily_parse_message_dag'

dag = makeDag("emr_test")


def add_scala_steps(jar_path, class_name, action='CONTINUE', criteria='', *args):
    """
    Define the EMR steps for scala version EmrAddStepsOperator
    :return: array
    """
    steps = [{
        'Name': class_name,
        'ActionOnFailure': action,
        'HadoopJarStep': {
            'Jar': 's3://ap-south-1.elasticmapreduce/libs/script-runner/script-runner.jar',
            'Args': [
                        '/usr/lib/spark/bin/spark-submit',
                        '--deploy-mode', 'cluster',
                        '--properties-file', '/etc/spark/conf/spark-defaults.conf',
                        '--conf', 'spark.yarn.executor.memoryOverhead=2048',
                        '--conf', 'spark.executor.memory=4g',
                        '--conf', 'spark.driver.memory=4g',
                        '--conf', 'spark.network.timeout=800',
                        '--class', '{}'.format(class_name),
                        jar_path,
                        criteria
                    ] + list(args)
        }
    }]
    return steps


def add_emrfs_clean_steps(name, action='CONTINUE'):
    return [{
        'Name': name,
        'ActionOnFailure': action,
        'HadoopJarStep': {
            'Jar': 's3://ap-south-1.elasticmapreduce/libs/script-runner/script-runner.jar',
            'Args': [
                '/usr/bin/emrfs',
                'delete', 's3://tb.es/'
            ]
        }
    }]

def add_cluster_resize_steps(name, task_id, task_count, action='CONTINUE'):
    return [{
        'Name': name,
        'ActionOnFailure': action,
        'HadoopJarStep': {
            'Jar': 's3://ap-south-1.elasticmapreduce/libs/script-runner/script-runner.jar',
            'Args': [
                '/usr/bin/aws', 'emr', 'modify-instance-groups', '--instance-groups'
                , 'InstanceGroupId={},InstanceCount={}'.format(task_id, task_count)
            ]
        }
    }]

def add_cluster_instance_fleet_resize_steps(name, cluster_id, instance_fleet_id,
                                            target_on_demand_capacity, target_spot_capacity, action='CONTINUE'):
    return [{
        'Name': name,
        'ActionOnFailure': action,
        'HadoopJarStep': {
            'Jar': 's3://ap-south-1.elasticmapreduce/libs/script-runner/script-runner.jar',
            'Args': [
                '/usr/bin/aws', 'emr', 'modify-instance-fleet', '--cluster-id', '{}'.format(cluster_id),
                '--instance-fleet', 'InstanceFleetId={},TargetOnDemandCapacity={},TargetSpotCapacity={}'.format(
                    instance_fleet_id, target_on_demand_capacity, target_spot_capacity)
            ]
        }
    }]


step_1 = EmrAddStepsOperator(
    task_id='step_1',
    aws_conn_id='aws_default',
    steps=add_scala_steps('jar-location',
                          'class-name', 'CONTINUE',
                          "{{ dag_run.conf['date'] }}"),
    dag=dag
)

sensor_1 = EmrStepSensor(
    task_id='sensor_1',
    job_flow_id="{{ dag_run.conf['cluster_id'] }}",
    step_id="{{ task_instance.xcom_pull('step_1', key='return_value')[0] }}",
    aws_conn_id='aws_default',
    dag=dag
)

step_2 = EmrAddStepsOperator(
    task_id='step_2',
    aws_conn_id='aws_default',
    steps=add_scala_steps('jar-location',
                          'class-name', 'CONTINUE',
                          "{{ dag_run.conf['date'] }}", "{{ dag_run.conf['date'] }}"),
    dag=dag
)

sensor_2 = EmrStepSensor(
    task_id='sensor_daily_parse_message',
    job_flow_id="{{ dag_run.conf['cluster_id'] }}",
    step_id="{{ task_instance.xcom_pull('step_2', key='return_value')[0] }}",
    aws_conn_id='aws_default',
    dag=dag
)

step_1 >> sensor_1 >> step_2 >> sensor_2
