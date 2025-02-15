from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import logging
import json
from openai import OpenAI
import re  # Se usará para extraer JSON

# Configuración de logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Configuración de la base de datos (Amazon RDS)
DB_CONFIG = {
    'host': 'db-tarragona-locations.cwebvv8rhxmt.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'contrasena',
    'database': 'Tarragona'
}

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        logging.error("Error al conectar a MySQL: %s", e)
        return None

@app.route('/procesarIA', methods=['POST'])
def deepseek_api():
    # Recibir la descripción del usuario
    descripcion_usuario = request.json.get('descripcion')

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",  # ¡IMPORTANTE! No exponer en producción
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

Devuelve solo un JSON con las puntuaciones (1-5) en cada categoría, por ejemplo:
{{"Assistencials": 3, "Culturals": 5, "Esportives": 4, "Estudis": 2, "MediAmbient": 3}}

Descripción del usuario:
"{descripcion_usuario}"

Respuesta JSON:"""
            }
        ]
    )

    # Obtener y limpiar la respuesta
    response_text = completion.choices[0].message.content.strip()
    logging.info("Respuesta de IA: %s", response_text)

    if not response_text:
        logging.error("Respuesta vacía de la IA")
        return jsonify({"error": "Respuesta vacía de la IA"}), 500

    # Intentar parsear la respuesta directamente como JSON
    try:
        ai_scores = json.loads(response_text)
    except json.JSONDecodeError as e:
        logging.error("Error al decodificar la respuesta de IA: %s", e)
        # Intentar extraer el JSON de la respuesta usando regex
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            try:
                ai_scores = json.loads(json_match.group())
            except json.JSONDecodeError as e2:
                logging.error("Error al decodificar JSON extraído: %s", e2)
                return jsonify({"error": "Formato de respuesta de IA inválido"}), 500
        else:
            logging.error("No se encontró formato JSON en la respuesta: %s", response_text)
            return jsonify({"error": "Formato de respuesta de IA inválido"}), 500

    # Aplicar la ponderación: 2^valor para cada categoría
    weighted_categories = {k: 2**v for k, v in ai_scores.items()}

    # Conectar a la base de datos y calcular los scores de las celdas
    conn = connect_db()
    if not conn:
        return jsonify({"error": "Error en la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM subdivision")
        grid_data = cursor.fetchall()

        scores = []
        for cell in grid_data:
            cell_id = cell['id']
            total_score = 0
            for category, weight in weighted_categories.items():
                category_count = cell.get(category, 0)  # Si no existe la columna, usa 0
                total_score += weight * category_count
            scores.append({"cell_id": cell_id, "score": total_score})

        # Ordenar por score descendente y seleccionar los 3 mejores
        scores_sorted = sorted(scores, key=lambda x: x['score'], reverse=True)[:3]

        # Devolver la respuesta con los top_cells y las puntuaciones originales de la IA
        return jsonify({"top_cells": scores_sorted, "ai_scores": ai_scores})

    except Error as e:
        logging.error("Error en la consulta: %s", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# (El resto del código permanece igual)
@app.route('/procesar', methods=['POST'])
def procesar():
    data = request.json
    weighted_categories = {k: 2**v for k, v in data.items()}

    conn = connect_db()
    if not conn:
        return jsonify({"error": "Error en la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM subdivision")
        grid_data = cursor.fetchall()

        scores = []
        for cell in grid_data:
            cell_id = cell['id']
            total_score = 0
            for category, weight in weighted_categories.items():
                category_count = cell.get(category, 0)
                total_score += weight * category_count
            scores.append({"cell_id": cell_id, "score": total_score})

        scores_sorted = sorted(scores, key=lambda x: x['score'], reverse=True)[:3]
        return jsonify({"top_cells": scores_sorted})
    
    except Error as e:
        logging.error("Error en la consulta: %s", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/cell_info/<int:cell_id>', methods=['GET'])
def cell_info(cell_id):
    conn = connect_db()
    if not conn:
        return jsonify({"error": "Error en la base de datos"}), 500
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM subdivision WHERE id = %s"
        cursor.execute(query, (cell_id,))
        result = cursor.fetchone()
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No se encontró la casilla"}), 404
    except Error as e:
        logging.error("Error en la consulta de cell_info: %s", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=False)
