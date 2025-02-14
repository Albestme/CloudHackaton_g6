import pandas as pd

# Cargar el CSV original (modifica el nombre o la ruta según corresponda)
archivo_csv = 'rectangulo.csv'
df = pd.read_csv(archivo_csv)

# Definir los límites del rectángulo principal
lat_max = 41.143083   # Arriba
lat_min = 41.107164   # Abajo
lng_min = 1.204506    # Izquierda
lng_max = 1.310221    # Derecha

# Filtrar los registros dentro del rectángulo principal
filtro_rect = (
    (df['ubicacio_location_lat'] >= lat_min) &
    (df['ubicacio_location_lat'] <= lat_max) &
    (df['ubicacio_location_lng'] >= lng_min) &
    (df['ubicacio_location_lng'] <= lng_max)
)
df_rect = df[filtro_rect]

# Lista de categorías posibles en la columna 'Seccio'
categorias = [
    # "Comunitàries / Cíviques",
    "Esportives",
    "Estudis, Formació i Recerca",
    "Assistencials",
    "Culturals",
    # "Cooperació / interacció",
    # "Socials",
    # "Econòmiques, Ocupacionals i Sindicals",
    # "Oci, Lleure, Agrupaments i Centres d'Esplai",
    # "Polítiques, Ideològiques i Religioses",
    "Medi Ambient, Ecologia i Sostenibilitat"
]

# Definir la subdivisión en 4 filas x 4 columnas
filas = 4
columnas = 4

# Tamaño de cada celda
tamaño_celda_lat = (lat_max - lat_min) / filas
tamaño_celda_lng = (lng_max - lng_min) / columnas

# Lista para acumular la información de cada subdivisión
info_subdivisiones = []

print("Generando subdivisiones (4x4):")
for fila in range(filas):
    # La fila 0 es la superior, por lo que:
    lat_superior = lat_max - (fila * tamaño_celda_lat)
    lat_inferior = lat_max - ((fila + 1) * tamaño_celda_lat)
    
    for col in range(columnas):
        lng_izquierda = lng_min + (col * tamaño_celda_lng)
        lng_derecha = lng_min + ((col + 1) * tamaño_celda_lng)
        
        # Número de la celda: se numeran de izquierda a derecha, de arriba a abajo
        celda_numero = fila * columnas + col
        
        # Filtrar los registros que caen dentro de la celda actual
        filtro_celda = (
            (df_rect['ubicacio_location_lat'] >= lat_inferior) &
            (df_rect['ubicacio_location_lat'] <= lat_superior) &
            (df_rect['ubicacio_location_lng'] >= lng_izquierda) &
            (df_rect['ubicacio_location_lng'] <= lng_derecha)
        )
        df_celda = df_rect[filtro_celda]
        
        # Guardar los registros de la celda en un archivo CSV con el nombre deseado
        nombre_archivo = f"subdisvision{celda_numero}.csv"
        df_celda.to_csv(nombre_archivo, index=False)
        
        # Contar los centros por cada categoría de 'Seccio'
        conteos = {}
        for categoria in categorias:
            # Contamos coincidencias exactas
            conteo = df_celda['Seccio'].eq(categoria).sum()
            # Creamos una columna con el prefijo n_ seguido del nombre de la categoría
            conteos[f"n_{categoria}"] = conteo
        
        # Definir las coordenadas de las esquinas de la celda
        coords_arriba_izq = f"{lat_superior}, {lng_izquierda}"
        coords_arriba_dch = f"{lat_superior}, {lng_derecha}"
        coords_abajo_izq = f"{lat_inferior}, {lng_izquierda}"
        coords_abajo_dch = f"{lat_inferior}, {lng_derecha}"
        
        # Guardar la información de la subdivisión
        info = {
            "subdivion": celda_numero,
            "coords_arriba_izq": coords_arriba_izq,
            "coords_arriba_dch": coords_arriba_dch,
            "coords_abajo_izq": coords_abajo_izq,
            "coords_abajo_dch": coords_abajo_dch,
        }
        info.update(conteos)
        info_subdivisiones.append(info)
        
        print(f"Celda {celda_numero}: {len(df_celda)} registros guardados en '{nombre_archivo}'.")

# Guardar la información agregada de todas las subdivisiones en un CSV resumen
df_info = pd.DataFrame(info_subdivisiones)
nombre_info = "subdivisiones_info.csv"
df_info.to_csv(nombre_info, index=False)
print(f"\nArchivo con información de subdivisiones generado: '{nombre_info}'.")
