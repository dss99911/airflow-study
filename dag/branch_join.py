import random

from airflow.operators.python import BranchPythonOperator

from operators.dags import *

dag = makeDag("branch_join_test")

run_this_first = DummyOperator(
    task_id='run_this_first',
    dag=dag,
)

options = ['branch_a', 'branch_b', 'branch_c', 'branch_d']

branching = BranchPythonOperator(
    task_id='branching',
    python_callable=lambda: random.choice(options),
    dag=dag,
)
run_this_first >> branching

join = DummyOperator(
    task_id='join',
    trigger_rule='none_failed_or_skipped',  # 실패나, 스킵인 경우, 처리를 안한다는 얘기인듯.. 보통 이전 테스크가 스킵되면, 다음 테스크는 수행되니까.
    # trigger_rule=TriggerRule.ALL_DONE,
    # trigger_rule='all_success',# 여러 브랜치 조인시, 모든 브랜치가 성공해야 하는 경우?, TODO 그러면, skip인 경우는 어떻게 되는거지?
    # trigger_rule='one_success',# 하나만 성공해도 되는 경우.
    dag=dag,
)

for option in options:
    t = DummyOperator(
        task_id=option,
        dag=dag,
    )

    dummy_follow = DummyOperator(
        task_id='follow_' + option,
        dag=dag,
    )

    branching >> t >> dummy_follow >> join
