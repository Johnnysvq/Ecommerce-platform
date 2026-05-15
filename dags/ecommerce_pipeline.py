from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


# Argumentos por defecto de todas las Tasks
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


# Definicion del DAG
dag = DAG(
    dag_id='ecommerce_pipeline',
    default_args=default_args,
    description='Pipeline completo del e-commerce: extract, transform, load, dbt',
    schedule_interval='0 6 * * *', # Todos los dias a las 6 am
    catchup=False,
    tags=['ecommerce', 'etl', 'dbt'],
)


# -- Task 1: extract data --
def run_extract(**context):
    import sys
    sys.path.insert(0, '/opt/airflow/src')
    from extract import extract_all

    data = extract_all()

    # Xcom: comparte datos entre tasks
    context['task_instance'].xcom_push(key='raw_data_summary', value={
        'products': len(data['products']),
        'users': len(data['users']),
        'orders': len(data['orders']),
        'extracted_at': data['extracted_at']
    })

    print(f"Extraidos: {len(data['products'])} productos, {len(data['users'])} usuarios, {len(data['orders'])} ordenes.")
    return "extract_complete"

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=run_extract,
    dag=dag,
)


# -- Task 2: transform + load --
def run_transform_load(**context):
    import sys
    sys.path.insert(0, '/opt/airflow/src')
    from extract import extract_all
    from transform import transform_all
    from load import load_all, load_to_snowflake

    # Re-extrae los datos (stateless pipeline)
    raw_data = extract_all()
    transformed_data = transform_all(raw_data)

    # Carga a PostgreSQL local
    load_all(transformed_data)

    # Carga a Snowflake RAW
    load_to_snowflake(transformed_data)

    print("Transform y load completados exitosamente.")
    return "transform_load_complete"

transform_load_task = PythonOperator(
    task_id='transform_and_load',
    python_callable=run_transform_load,
    dag=dag,
)


# -- Task 3: run dbt --
dbt_run_task = BashOperator(
    task_id='dbt_run',
    bash_command='cd /opt/airflow/ecommerce_dbt && dbt run --profiles-dir /opt/airflow/ecommerce_dbt',
    dag=dag,
)

# -- Task 4: run dbt tests --
dbt_test_task = BashOperator(
    task_id='dbt_test',
    bash_command='cd /opt/airflow/ecommerce_dbt && dbt test --profiles-dir /opt/airflow/ecommerce_dbt',
    dag=dag,
)

# -- Task 5: Verificacion final --
def run_validation(**context):
    summary = context['task_instance'].xcom_pull(
        task_ids='extraxt_data',
        key='raw_data_summary',
    )

    print(f"Pipeline completado exitosamente!")
    print(f"Resumen: {summary}")
    return "pipeline_complete"

validation_task = PythonOperator(
    task_id='validate_pipeline',
    python_callable=run_validation,
    dag=dag,
)


# -- Dependencias: define el orden de ejecucion --
extract_task >> transform_load_task >> dbt_run_task >> dbt_test_task >> validation_task