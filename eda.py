import os
from pyspark.sql import SparkSession

# 1. Crear e inicializar una SparkSession
# Es el punto de entrada para cualquier funcionalidad de Spark.
spark = SparkSession.builder \
    .appName("HackathonForecastEDA") \
    .master("local[*]") \
    .getOrCreate()

print(f"SparkSession iniciada. Versión de Spark: {spark.version}")

# 2. Define la ruta base y los directorios de datos
base_path = '/home/quind/GIT/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025'
directorios_datos = ['archivos1', 'archivos2', 'archivos3']

# Diccionario para almacenar los DataFrames de Spark
spark_dfs = {}

print("\nIniciando la lectura de los directorios con PySpark...")
print("="*60)

# 3. Itera sobre cada directorio para leer los datos
for directorio in directorios_datos:
    path_directorio = os.path.join(base_path, directorio)
    
    try:
        print(f" Leyendo datos del directorio: {path_directorio}")
        
        # 4. Leer el directorio de Parquet.
        # PySpark lee directamente el directorio y descubre los archivos 'part-' automáticamente.
        df = spark.read.parquet(path_directorio)
        
        # Almacena el DataFrame en el diccionario
        spark_dfs[directorio] = df
        
        # 5. Muestra información clave del DataFrame
        print(f"\n--- Exploración de datos en '{directorio}' ---")
        
        print("\n[Esquema del DataFrame (df.printSchema())]")
        df.printSchema()
        
        print("\n[Primeras 5 filas (df.show(5))]")
        # El argumento 'truncate=False' evita que se corten los valores largos en las columnas
        df.show(5, truncate=False)
        
        print(f"Número total de filas: {df.count()}")
        
        print("="*60 + "\n")

    except Exception as e:
        # En Spark, un error común al leer es AnalysisException si la ruta no existe
        print(f"ERROR: No se pudo leer el directorio '{path_directorio}'. Causa: {e}\n")

# 6. Detener la sesión de Spark para liberar recursos
# Es una buena práctica hacerlo al final de tu script.
spark.stop()
print("SparkSession detenida.")

# Ahora puedes acceder a cada Spark DataFrame usando su clave, por ejemplo:
# sdf_transacciones = spark_dfs['archivos1']
# sdf_productos = spark_dfs['archivos2']
# sdf_pdvs = spark_dfs['archivos3']