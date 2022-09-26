from ast import Sub
import queue
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from subdags.subdag_download import subdag_download
from subdags.subdag_transform import subdag_transform
 
from datetime import datetime
 
with DAG('group_dag', start_date=datetime(2022, 1, 1), 
    schedule_interval='@daily', catchup=False) as dag:

    args = {'schedule_interval':dag.schedule_interval,'start_date':dag.start_date,'catchup':dag.catchup}


    downloads =  SubDagOperator(
        task_id = 'downloads',
        subdag = subdag_download(dag.dag_id,'downloads',args)

    )
 
 
    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )
 
    transforms = SubDagOperator(task_id='transforms',
    subdag = subdag_transform(dag.dag_id,'transforms',args)
    )
 
    downloads >> check_files >> transforms