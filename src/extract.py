import requests
import json
import logging
from datetime import datetime

# Configuracion de los logs - En produccion siemore se loggea todo

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_products() -> list[dict]:
    """
    Extrae los productos de la API de Fake Store.
    Retorna una lista de diccionarios con los datos crudos.
    """

    url = "https://fakestoreapi.com/products"

    logger.info(f"Extrayendo los productos de la API: {url}")

    response = requests.get(url, timeout=10)

    response.raise_for_status()  # Lanza una excepción si la API falla

    products = response.json()
    logger.info(f"Productos extraidos: {len(products)}")

    return products

def extract_users() -> list[dict]:
    """
    Extrae los usuarios de la API de Fake Store.
    """
    url = "https://fakestoreapi.com/users"
    logger.info(f"Extrayendo los usuarios de: {url}")

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    users = response.json()
    logger.info(f"Usuarios extraidos: {len(users)}")

    return users


def extract_orders() -> list[dict]:
    """
    Extrae todas las ordenes (carts) de la Fake Store API.
    """

    url = "https://fakestoreapi.com/carts"
    logger.info(f"Extrayendo las ordenes de: {url}")

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    orders = response.json()
    logger.info(f"Ordenes extraidas: {len(orders)}")
    
    return orders


def extract_all() -> dict:
    """
    Funcion principal que extrae todas las entidades.
    Retorna un diccionario con todos los datos crudos.
    """

    logger.info("Aqui se inicia la extraccion completa")

    data = {
        "products": extract_products(),
        "users": extract_users(),
        "orders": extract_orders(),
        "extracted_at": datetime.now().isoformat()
    }

    logger.info("Extraccion completa")
    return data

if __name__ == "__main__":
    data = extract_all()

    # Se imprime un resumen de lo que extrajimos
    print("\n=== RESUMEN DE EXTRACCIÓN ===")
    print(f"Productos:  {len(data['products'])}")
    print(f"Usuarios:   {len(data['users'])}")
    print(f"Órdenes:    {len(data['orders'])}")
    print(f"Extraído a: {data['extracted_at']}")

    # Muestra un ejemplo de cada entidad
    print("\n--- EJEMPLO DE PRODUCTO ---")
    print(json.dumps(data['products'][0], indent=2))

    print("\n--- EJEMPLO DE ORDEN ---")
    print(json.dumps(data['orders'][0], indent=2))