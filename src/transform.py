import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def transform_products(raw_products: list[dict]) -> pd.DataFrame:
    """
    Transforma la lista cruda de productos en un DataFrame limpio.
    """

    logger.info("Transformando productos...")

    df = pd.DataFrame(raw_products)

    # El campo rating viene anidado en: {"rate": 3.9, "count": 120}
    # Entonces se convierá en dos columnas separadas
    df['rating_rate'] = df['rating'].apply(lambda x: x['rate'])
    df['rating_count'] = df['rating'].apply(lambda x: x['count'])
    df = df.drop(columns=['rating'])

    # Limpieza de tipos de datos
    df['price'] = df['price'].astype(float).round(2)
    df['rating_rate'] = df['rating_rate'].astype(float)
    df['rating_count'] = df['rating_count'].astype(int)

    # Estandarizado de texto: minusculas y sin espacios al inicio ni al final
    df['title'] = df['title'].str.strip()
    df['category'] = df['category'].str.strip().str.lower()

    # Columna de auditoria
    # Se agrega para saber cuando fue procesado este registro\
    df['loaded_at'] = datetime.now()

    # Renombra las columnas a snake_case
    df = df.rename(columns={'id': 'product_id'})

    logger.info(f"Productos transformados: {len(df)} filas, {len(df.columns)} columnas")

    return df


def transform_users(raw_users: list[dict]) -> pd.DataFrame:
    """
    Transforma la lista cruda de usuarios en un DataFrame limpio.
    los usuarios tienen datos muy anidados, por lo que se deben extraer y normalizar
    """

    logger.info("Transformando usuarios..")

    df = pd.DataFrame(raw_users)

    # Se convierten las columnas anidadas firstname y lastname en columnas aparte
    df['first_name'] = df['name'].apply(lambda x: x['firstname'].strip().title())
    df['last_name'] = df['name'].apply(lambda x: x['lastname'].strip().title())
    df['full_name'] = df['first_name'] + ' ' + df['last_name']

    # 'address' viene anidado con geolocation adentro
    df['city'] = df['address'].apply(lambda x: x['city'].strip().title())
    df['street'] = df['address'].apply(lambda x: x['street'].strip())
    df['zipcode'] = df['address'].apply(lambda x: x['zipcode'].strip())
    df['geo_lat'] = df['address'].apply(lambda x: float(x['geolocation']['lat']))
    df['geo_long'] = df['address'].apply(lambda x: float(x['geolocation']['long']))

    # Limpiar el email
    df['email'] = df['email'].str.strip().str.lower()

    # Se eliminan las columnas anidadas que ya se procesaron
    df = df.drop(columns=['name', 'address'])

    # Columna de auditoria
    df['loaded_at'] = datetime.now()

    df = df.rename(columns={'id': 'user_id'})

    logger.info(f"Usuarios transformados: {len(df)} filas, {len(df.columns)} columnas")

    return df


def transform_orders(raw_orders: list[dict]) -> pd.DataFrame:
    """
    Transforma la lista de ordenes. Cada orden tiene multiples productos
    en una lista - las expandimos para tener una fila por producto.
    """

    logger.info("Transformando ordenes...")

    # Primero se aplanan los productos de cada orden
    # Cada orden tiene: {id, userId, date, products: [{productId, quantity}]}

    rows = []

    for order in raw_orders:
        for product in order['products']:
            rows.append({
                'order_id': order['id'],
                'user_id': order['userId'],
                'order_date': order['date'],
                'product_id': product['productId'],
                'quantity': product['quantity']
            })

    df = pd.DataFrame(rows)

    # Convierte la fecha a tipo datetime
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Asegura tipos correctos
    df['quantity'] = df['quantity'].astype(int)

    # Columna de auditoria
    df['loaded_at'] = datetime.now()

    logger.info(f"Ordenes transformadas: {len(df)} filas, {len(df.columns)} columnas")

    return df


def transform_all(raw_data: dict) -> dict:
    """
    Transforma todos los datasets y los retorna como DataFrames limpios.
    """

    logger.info("Iniciando transformaciones")

    transformed = {
        "products": transform_products(raw_data['products']),
        "users": transform_users(raw_data['users']),
        "orders": transform_orders(raw_data['orders'])
    }

    logger.info("Transformaciones completadas")
    return transformed


if __name__ == "__main__":

    # Importamos extract para poder probar el pipeline completo
    from extract import extract_all

    raw_data = extract_all()
    clean_data = transform_all(raw_data)

    # Inspeccionamos los resultados
    print("\n=== PRODUCTOS LIMPIOS ===")
    print(clean_data["products"].dtypes)
    print(clean_data["products"].head(3))

    print("\n=== USUARIOS LIMPIOS ===")
    print(clean_data["users"].columns.tolist())
    print(clean_data["users"].head(3))

    print("\n=== ÓRDENES LIMPIAS ===")
    print(clean_data["orders"].head(10))
