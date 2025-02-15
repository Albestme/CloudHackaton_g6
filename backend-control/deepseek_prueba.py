from openai import OpenAI

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

deepseek_api("Me gustan los parques y las actividades al aire libre, pero no me interesan los museos ni las bibliotecas.")