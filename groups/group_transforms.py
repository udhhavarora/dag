from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup


def transform_tasks():
    with TaskGroup('transforms',tooltip='Transforms Group') as group:

        transform_a = BashOperator(
            task_id = 'transform_a',
            queue = 'high_cpu',
            bash_command='sleep 10'
        )

        transform_b = BashOperator(
            task_id = 'transform_b',
            queue = 'high_cpu',
            bash_command='sleep 10'
        )

        transform_b = BashOperator(
            task_id = 'transform_c',
            queue = 'high_cpu',
            bash_command='sleep 10'
        )

        return group