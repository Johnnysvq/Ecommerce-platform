import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_large_orders(n_records: int = 1_000_000) -> pd.DataFrame:
    """
    Genera n_records de ordenes sinteticas realistas.
    1 millon de registros por defecto.
    """
    logger.info(f"Generando {n_records:,} ordenes sinteticas... ")

    np.random.seed(43)

    # Distribucion realiosta de usuarios (pocos usuarios comprando mucho)
    user_ids = np.random.zipf(1.5, n_records) % 1000 + 1 # 1000 usuarios unicos
    product_ids = np.random.zipf(1.3, n_records) % 20 + 1 # 20 productos unicos

    # Fechas en los ultimos 2 anios
    start_date = datetime(2023, 1, 1)
    days = np.random.randint(0, 730, n_records)
    dates = [start_date + timedelta(days=int(d)) for d in days]

    df = pd.DataFrame({
        'order_id':   range(1, n_records + 1),
        'user_id':    user_ids,
        'product_id': product_ids,
        'quantity':   np.random.randint(1, 11, n_records),
        'order_date': dates,
        'country':    np.random.choice(
            ['US', 'MX', 'CR', 'CO', 'BR', 'AR', 'CL', 'PE'],
            n_records,
            p=[0.4, 0.15, 0.05, 0.1, 0.1, 0.08, 0.07, 0.05]
        ),
        'device':     np.random.choice(
            ['mobile', 'desktop', 'tablet'],
            n_records,
            p=[0.6, 0.3, 0.1]
        ),
        'status':     np.random.choice(
            ['completed', 'cancelled', 'returned', 'pending'],
            n_records,
            p=[0.75, 0.1, 0.08, 0.07]
        )
    })

    logger.info(f"Datos generados: {len(df):,} filas, {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB de memoria")
    return df

if __name__ == "__main__":
    df = generate_large_orders(1_000_000)

    # Guarda como parquet, que es el formato estandar en Big Data
    output_path = "data/large_orders.parquet"
    import os
    os.makedirs("data", exist_ok=True)
    df.to_parquet(output_path, index=False)

    logger.info(f"Guardado en {output_path}")
    print(f"\nResumen:")
    print(f"  Total ordenes:    {len(df):,}")
    print(f"  Usuarios unicos:  {df['user_id'].nunique():,}")
    print(f"  Productos unicos: {df['product_id'].nunique():,}")
    print(f"  Rango de fechas:  {df['order_date'].min()} → {df['order_date'].max()}")
    print(f"  Por status:")
    print(df['status'].value_counts())