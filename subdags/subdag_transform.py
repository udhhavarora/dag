from airflow import DAG
from airflow.operators.bash import BashOperator

def subdag_transform(parent_dag_id,child_dag_id,args):
    with DAG(f"{parent_dag_id}.{child_dag_id}", start_date=args['start_date'],schedule_interval=args['schedule_interval'],
        catchup=args['catchup']) as dag:

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

        return dag