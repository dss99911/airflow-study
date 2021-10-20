import pytest

from airflow.models import DagBag


@pytest.fixture()
def dagbag():
    return DagBag()


def assert_dag_dict_equal(source, dag):
    assert dag.task_dict.keys() == source.keys()
    for task_id, downstream_list in source.items():
        assert dag.has_task(task_id)
        task = dag.get_task(task_id)
        assert task.downstream_task_ids == set(downstream_list)


def get_dict_string(dag):
    list_dag_downstream = list(map(lambda k: f"'{k}':{list(dag.task_dict[k].downstream_task_ids)}", dag.task_dict))
    return "{\n" + (",\n".join(list_dag_downstream)) + "}"
