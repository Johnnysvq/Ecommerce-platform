import logging
import os
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
# Carga las variables de entorno
load_dotenv(override=True, encoding='utf-8')

def get_engine():
    engine = create_engine(
        f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    logger.info("Conexión a PostgreSQL establecida")
    return engine

def create_tables(engine):
    """
    Crea las tablas en PostgreSQL si no existen.
    Lee el archivo SQl que definimos arriba.
    """

    logger.info("Creando tablas en PostgreSQL...")

    # Busca el archivo SQL relativo a la raiz del proyecto
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'create_tables.sql')

    with open(sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    logger.info("Tablas creadas exitosamente")


def load_dataframe(df:pd.DataFrame, table_name:str, engine):
    """
    Carga un DataFrame a una tabla de PostgreSQl.
    
    if_exists='replace' -> borra y recrea la tabla cada vez
    """

    logger.info(f"Cargando {len(df)} filas a la tabla '{table_name}'...")

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='replace', # reemplaza los datos existente
        index=False,         # no guarda el indice de pandas como columna
        method='multi',      # inserta multiples filas por query (mas rapido)
        chunksize=1000       # inserta de a 1000 filas a la vez
    )

    logger.info(f"Tabla '{table_name}' cargada exitosamente")


def verify_load(engine):
    """
    Verifica que los datos se cargaron correctamente
    Buenas practicas: siempre verificar después de cargar
    """

    logger.info("Verificando carga de datos...")

    tables = ['products', 'users', 'orders']

    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            logger.info(f"Tabla {table}: {count} filas")


def load_all(transformed_data: dict) -> None:
    """
    Funcion principal: orquesta toda la data
    """

    logger.info("Iniciando el proceso de carga...")

    engine = get_engine()
    create_tables(engine)

    load_dataframe(transformed_data['products'], 'products', engine)
    load_dataframe(transformed_data['users'], 'users', engine)
    load_dataframe(transformed_data['orders'], 'orders', engine)

    verify_load(engine)

    logger.info("Proceso de carga completado")


if __name__ == "__main__":
    from extract import extract_all
    from transform import transform_all

    raw_data = extract_all()
    transformed_data = transform_all(raw_data)
    load_all(transformed_data)