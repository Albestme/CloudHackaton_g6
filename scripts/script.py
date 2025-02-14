import pandas as pd

# Cargar el CSV (asegúrate de que el archivo esté en el mismo directorio o indica la ruta completa)
archivo_csv = 'data.csv'  # Cambia este nombre por el de tu archivo
df = pd.read_csv(archivo_csv)

# Mostrar los tipos únicos que hay en la columna 'Seccio'
print("Tipos disponibles en la columna 'Seccio':")
print(df['Seccio'].unique())

# Solicitar al usuario que ingrese el tipo de sección a filtrar
seccion_filtrar = input("Ingresa el tipo de Seccio a filtrar (ej. Esportives): ").strip()

# Filtrar el DataFrame según la sección ingresada (ignorando mayúsculas/minúsculas)
filtro = df['Seccio'].str.contains(seccion_filtrar, case=False, na=False)
df_filtrado = df[filtro]

# Generar el nombre del archivo de salida basado en la sección ingresada (por ejemplo, 'esportives.csv')
nombre_archivo = f"{seccion_filtrar.lower()}.csv"

# Exportar el DataFrame filtrado a CSV sin el índice
df_filtrado.to_csv(nombre_archivo, index=False)

print(f"El archivo con los registros filtrados se ha guardado como {nombre_archivo}")
