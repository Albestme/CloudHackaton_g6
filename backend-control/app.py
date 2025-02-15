from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configuración de la base de datos (Amazon RDS)
DB_CONFIG = {
    'host': 'db-tarragona-locations.cwebvv8rhxmt.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'contrasena',
    'database': 'Tarragona',
    #'port': 3306
}

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("Error al conectar a MySQL:", e)
        return None
    
def deepseek_api(descripcion_usuario):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    )

    completion = client.chat.completions.create(
    model="deepseek/deepseek-r1:free",
    messages=[
        {
        "role": "user",
        "content": f"""Eres un sistema que convierte descripciones de preferencias personales en puntuaciones del 1 al 5 para categorías de vivienda.
        Las categorías son:
        - Assistencials (Servicios asistenciales como salud, farmacias, hospitales)
        - Culturals (Museos, teatros, actividades culturales)
        - Esportives (Instalaciones deportivas, gimnasios, actividades al aire libre)
        - Estudis (Colegios, universidades, bibliotecas)
        - MediAmbient (Zonas verdes, parques, naturaleza)

        Devuelve solo un JSON con las puntuaciones del 1 al 5 en cada categoría, por ejemplo:
        {{"Assistencials": 3, "Culturals": 5, "Esportives": 4, "Estudis": 2, "MediAmbient": 3}}

        Descripción del usuario:
        "{descripcion_usuario}"

        Respuesta JSON:"""
        }
    ]
    )
    print(completion.choices[0].message.content)

@app.route('/procesar', methods=['POST'])
def procesar():
    # Recibir JSON del frontend y aplicar ponderación 2^valor
    data = request.json
    weighted_categories = {k: 2**v for k, v in data.items()}
    
    # Conectar a la base de datos
    conn = connect_db()
    if not conn:
        return jsonify({"error": "Error en la base de datos"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Consultar TODAS las celdas de la matriz (16)
        cursor.execute("SELECT * FROM subdivision")  # Asume tabla 'subdivision' con columnas: id, Assistencials, Culturals, Esportives, Estudis, MediAmbient
        grid_data = cursor.fetchall()
        
        scores = []
        # Calcular el grid score para cada celda
        for cell in grid_data:
            cell_id = cell['id']
            total_score = 0
            
            # Multiplicar cada categoría ponderada por su valor en la celda
            for category, weight in weighted_categories.items():
                category_count = cell.get(category, 0)  # Si no existe, usa 0
                total_score += weight * category_count
            
            scores.append({"cell_id": cell_id, "score": total_score})
        
        # Ordenar por score descendente y seleccionar top 3
        scores_sorted = sorted(scores, key=lambda x: x['score'], reverse=True)[:3]
        
        return jsonify({"top_cells": scores_sorted})
    
    except Error as e:
        print("Error en la consulta:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=False)