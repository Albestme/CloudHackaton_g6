import pandas as pd

# Nombre del archivo CSV de entrada (modifícalo según corresponda)
archivo_csv = 'data.csv'
df = pd.read_csv(archivo_csv)

# Definir los límites del rectángulo
lat_min = 41.107164
lat_max = 41.143083
lng_min = 1.204506
lng_max = 1.310221

# Filtrar las filas cuyos valores de latitud y longitud se encuentran dentro del rectángulo
filtro_rect = (
    (df['ubicacio_location_lat'] >= lat_min) &
    (df['ubicacio_location_lat'] <= lat_max) &
    (df['ubicacio_location_lng'] >= lng_min) &
    (df['ubicacio_location_lng'] <= lng_max)
)
df_rect = df[filtro_rect]

# Guardar el resultado en un nuevo archivo CSV
nombre_salida = 'rectangulo.csv'
df_rect.to_csv(nombre_salida, index=False)

print(f"Se ha generado el archivo '{nombre_salida}' con las ubicaciones dentro del rectángulo.")
