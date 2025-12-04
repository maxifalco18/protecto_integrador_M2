import pandas as pd
import os

# Configuración
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DB Proyecto', 'csv')

def analyze_csvs():
    print("=== INICIO DE ANÁLISIS EXPLORATORIO DE DATOS (EDA) ===\n")
    
    if not os.path.exists(DATA_DIR):
        print(f"Error: No se encuentra el directorio {DATA_DIR}")
        return

    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    files.sort()

    for file in files:
        file_path = os.path.join(DATA_DIR, file)
        print(f"--- Analizando: {file} ---")
        try:
            # Intentar leer con diferentes encodings si falla utf-8
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='latin-1')
            
            print(f"Dimensiones: {df.shape[0]} filas, {df.shape[1]} columnas")
            print("\nColumnas y Tipos de Datos:")
            print(df.dtypes)
            
            print("\nValores Nulos por Columna:")
            nulls = df.isnull().sum()
            print(nulls[nulls > 0])
            
            print("\nPrimeras 3 filas:")
            print(df.head(3))
            print("\n" + "="*50 + "\n")
            
        except Exception as e:
            print(f"Error al leer {file}: {e}\n")

if __name__ == "__main__":
    analyze_csvs()
