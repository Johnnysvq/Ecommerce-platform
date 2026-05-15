FROM apache/airflow:2.8.1

USER airflow

RUN pip install --no-cache-dir \
    pg8000==1.30.3 \
    snowflake-sqlalchemy==1.9.0 \
    snowflake-connector-python==3.6.0 \
    dbt-core==1.7.0 \
    dbt-snowflake==1.7.0