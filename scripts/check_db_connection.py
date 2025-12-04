import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def check_connection():
    print(f"Intentando conectar a {DB_HOST}:{DB_PORT}...")
    
    # Cadena de conexión para SQLAlchemy
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    try:
        # Intentar conectar usando SQLAlchemy
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("¡Conexión exitosa a la base de datos!")
            print(f"Base de datos: {DB_NAME}")
            print(f"Usuario: {DB_USER}")
            
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        print("\nSugerencia: Verifica que el contenedor/servicio de Postgres esté corriendo y que la base de datos haya sido creada.")

if __name__ == "__main__":
    check_connection()
