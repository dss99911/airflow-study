from test.dag_test import *


def test_dag_loaded(dagbag):
    dag = dagbag.get_dag(dag_id="bash_operator")
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 4
    assert_dag_dict_equal(
        {
            'print_date': ['sleep'],
            'sleep': ['templated'],
            'templated': [],
        },
        dag,
    )