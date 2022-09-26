from airflow import DAG
from airflow.operators.python import PythonOperator,BranchPythonOperator
from airflow.operators.bash import BashOperator
 
from datetime import datetime
 
def _t1():
    return 42

def _t1_n(ti):
    ti.xcom_push(key='ud_key',value=13)

def _branch(ti):
    value = ti.xcom_pull(key='ud_key',task_ids= 't1_n') 
    if (value == 13):
        return 't2'
    else:
        return 't3'

def _t2(ti):
    print(ti.xcom_pull(key='ud_key',task_ids = 't1_n'))
 
with DAG("xcom_dag", start_date=datetime(2022, 1, 1), 
    schedule_interval='@daily', catchup=False) as dag:
 
    t1 = PythonOperator(
        task_id='t1',
        python_callable=_t1
    )

    t1_n = PythonOperator(
        task_id='t1_n',
        python_callable=_t1_n
    )

    branch = BranchPythonOperator(
        task_id = 'branch',
        python_callable = _branch
    )
 
    t2 = PythonOperator(
        task_id='t2',
        python_callable=_t2
    )
 
    t3 = BashOperator(
        task_id='t3',
        bash_command="echo ''"
    )

    t4 = BashOperator(
        task_id='t4',
        bash_command="echo ''",
        trigger_rule='all_success'
    )
 
    t1 >> t1_n >> branch >> [t2, t3] >>t4