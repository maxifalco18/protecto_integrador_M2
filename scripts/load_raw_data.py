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

# Directorio de datos
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DB Proyecto', 'csv')

def get_engine():
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

def create_tables(engine):
    print("Creando tablas en la base de datos...")
    
    # DDL adaptado a PostgreSQL
    ddl_commands = """
    -- Tabla: Usuarios
    CREATE TABLE IF NOT EXISTS Usuarios (
        UsuarioID SERIAL PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL,
        Apellido VARCHAR(100) NOT NULL,
        DNI VARCHAR(20) UNIQUE NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL,
        Contraseña VARCHAR(255) NOT NULL,
        FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Tabla: Categorías
    CREATE TABLE IF NOT EXISTS Categorias (
        CategoriaID SERIAL PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL,
        Descripcion VARCHAR(255)
    );

    -- Tabla: Productos
    CREATE TABLE IF NOT EXISTS Productos (
        ProductoID SERIAL PRIMARY KEY,
        Nombre VARCHAR(255) NOT NULL,
        Descripcion TEXT,
        Precio DECIMAL(10,2) NOT NULL,
        Stock INT NOT NULL,
        CategoriaID INT REFERENCES Categorias(CategoriaID)
    );

    -- Tabla: Órdenes
    CREATE TABLE IF NOT EXISTS Ordenes (
        OrdenID SERIAL PRIMARY KEY,
        UsuarioID INT REFERENCES Usuarios(UsuarioID),
        FechaOrden TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Total DECIMAL(10,2) NOT NULL,
        Estado VARCHAR(50) DEFAULT 'Pendiente'
    );

    -- Tabla: Detalle de Órdenes
    CREATE TABLE IF NOT EXISTS DetalleOrdenes (
        DetalleID SERIAL PRIMARY KEY,
        OrdenID INT REFERENCES Ordenes(OrdenID),
        ProductoID INT REFERENCES Productos(ProductoID),
        Cantidad INT NOT NULL,
        PrecioUnitario DECIMAL(10,2) NOT NULL
    );

    -- Tabla: Métodos de Pago
    CREATE TABLE IF NOT EXISTS MetodosPago (
        MetodoPagoID SERIAL PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL,
        Descripcion VARCHAR(255)
    );
    
    -- Tabla: Carrito (Opcional para DW, pero está en los datos)
    CREATE TABLE IF NOT EXISTS Carrito (
        CarritoID SERIAL PRIMARY KEY,
        UsuarioID INT REFERENCES Usuarios(UsuarioID),
        ProductoID INT REFERENCES Productos(ProductoID),
        Cantidad INT NOT NULL,
        FechaAgregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Tabla: Reseñas de Productos
    CREATE TABLE IF NOT EXISTS ResenasProductos (
        ResenaID SERIAL PRIMARY KEY,
        UsuarioID INT REFERENCES Usuarios(UsuarioID),
        ProductoID INT REFERENCES Productos(ProductoID),
        Calificacion INT CHECK (Calificacion >= 1 AND Calificacion <= 5),
        Comentario TEXT,
        Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Tabla: Historial de Pagos
    CREATE TABLE IF NOT EXISTS HistorialPagos (
        PagoID SERIAL PRIMARY KEY,
        OrdenID INT REFERENCES Ordenes(OrdenID),
        MetodoPagoID INT REFERENCES MetodosPago(MetodoPagoID),
        Monto DECIMAL(10,2) NOT NULL,
        FechaPago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        EstadoPago VARCHAR(50)
    );

    -- Tabla: Ordenes Metodos Pago (Tabla intermedia detectada en CSV)
    CREATE TABLE IF NOT EXISTS OrdenesMetodosPago (
        OrdenID INT REFERENCES Ordenes(OrdenID),
        MetodoPagoID INT REFERENCES MetodosPago(MetodoPagoID),
        MontoPagado DECIMAL(10,2),
        PRIMARY KEY (OrdenID, MetodoPagoID)
    );
    """    # Usar engine.begin() para manejar la transacción automáticamente (compatible con SQLAlchemy 1.4 y 2.0)
    with engine.begin() as connection:
        connection.execute(text(ddl_commands))
    print("Tablas creadas exitosamente.")

def load_data(engine):
    # Mapeo de archivo CSV a nombre de tabla SQL
    # El orden es importante por las claves foráneas
    files_map = [
        ('1.Usuarios.csv', 'usuarios'),
        ('2.Categorias.csv', 'categorias'),
        ('3.Productos.csv', 'productos'),
        ('4.ordenes.csv', 'ordenes'),
        ('5.detalle_ordenes.csv', 'detalleordenes'),
        ('8.metodos_pago.csv', 'metodospago'),
        ('7.carrito.csv', 'carrito'),
        ('10.resenas_productos.csv', 'resenasproductos'),
        ('11.historial_pagos.csv', 'historialpagos'),
        ('9.ordenes_metodospago.csv', 'ordenesmetodospago')
    ]

    for csv_file, table_name in files_map:
        file_path = os.path.join(DATA_DIR, csv_file)
        if not os.path.exists(file_path):
            print(f"Advertencia: Archivo {csv_file} no encontrado. Saltando...")
            continue

        print(f"Cargando {csv_file} en tabla '{table_name}'...")
        
        try:
            # Leer CSV
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='latin-1')
            
            # Limpieza básica si es necesaria (ej: fechas)
            # Pandas suele manejar bien los tipos, pero a veces hay que forzar
            
            # Convertir columnas a minúsculas para compatibilidad con Postgres
            df.columns = [c.lower() for c in df.columns]

            # Cargar a SQL
            # if_exists='append' para agregar a la tabla creada
            # index=False porque ya tenemos IDs en los CSVs o son autogenerados (cuidado aquí)
            
            # NOTA: Si los CSVs ya traen IDs primarios, hay que tener cuidado con los SERIAL.
            # En este caso, los CSVs parecen traer IDs.
            # Postgres permite insertar en columnas SERIAL si se especifican explícitamente.
            
            with engine.begin() as connection:
                df.to_sql(table_name, connection, if_exists='append', index=False, method='multi', chunksize=1000)
            print(f"Cargados {len(df)} registros en {table_name}.")
            
        except Exception as e:
            print(f"Error cargando {csv_file}: {e}")

def main():
    engine = get_engine()
    create_tables(engine)
    load_data(engine)
    print("\n=== PROCESO DE CARGA FINALIZADO ===")

if __name__ == "__main__":
    main()
