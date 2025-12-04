import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_engine():
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

def check_data_quality(engine):
    print("=== REPORTE DE CALIDAD DE DATOS (POSTGRES) ===\n")
    
    tables_to_check = [
        ('usuarios', 'usuarioid'),
        ('categorias', 'categoriaid'),
        ('productos', 'productoid'),
        ('ordenes', 'ordenid'),
        ('detalleordenes', 'detalleid'),
        ('metodospago', 'metodopagoid'),
        ('resenasproductos', 'resenaid'),
        ('historialpagos', 'pagoid')
    ]

    with engine.connect() as connection:
        for table, pk in tables_to_check:
            print(f"--- Tabla: {table} ---")
            
            # 1. Conteo de filas
            count_query = text(f"SELECT COUNT(*) FROM {table}")
            total_rows = connection.execute(count_query).scalar()
            print(f"Total filas: {total_rows}")
            
            # 2. Chequeo de Duplicados en PK
            dup_query = text(f"""
                SELECT {pk}, COUNT(*) 
                FROM {table} 
                GROUP BY {pk} 
                HAVING COUNT(*) > 1
            """)
            dups = connection.execute(dup_query).fetchall()
            if dups:
                print(f"ALERTA: {len(dups)} duplicados encontrados en PK {pk}")
            else:
                print(f"PK {pk}: Sin duplicados")
                
            # 3. Chequeo de Nulos (Muestra de todas las columnas)
            # Obtenemos columnas
            cols_query = text(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table}'
            """)
            columns = [row[0] for row in connection.execute(cols_query)]
            
            null_found = False
            for col in columns:
                null_query = text(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL")
                null_count = connection.execute(null_query).scalar()
                if null_count > 0:
                    print(f"  - Columna '{col}': {null_count} nulos")
                    null_found = True
            
            if not null_found:
                print("  - Sin valores nulos detectados")
            
            print("")

if __name__ == "__main__":
    engine = get_engine()
    check_data_quality(engine)
