import json
import os
from groq import Groq

# Configuración de Groq (reemplaza Hugging Face — mismo resultado, gratis y más rápido)
client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"  # Llama 3.3 70B disponible en Groq (gratis)


def read_game_telemetry(file_path):
    """Lee la data simulada del videojuego."""
    with open(file_path, "r") as file:
        return json.load(file)


def query_ai_model(system_prompt, user_prompt):
    """Envía la solicitud al modelo de IA (Groq — Gratis)."""
    print(f"Conectando con el Cerebro Musical (Groq / {MODEL})...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content


def generate_musicxml_scaffold(game_data):
    """Prepara el prompt y procesa la respuesta de la IA."""

    system_prompt = (
        "Eres un Compositor Asistente Técnico y experto en teoría musical. "
        "Tu tarea es recibir datos de telemetría de un videojuego y generar UNICAMENTE "
        "un código MusicXML válido y limpio. El código debe representar un andamiaje musical "
        "(un compás o frase corta) que sirva de punto de partida para el compositor humano. "
        "Adapta el tempo, la tonalidad y la armonía según la emoción del juego. "
        "NO escribas explicaciones ni texto fuera del XML."
    )
    user_prompt = (
        f"Telemetría actual del juego: {json.dumps(game_data)}. "
        "Genera el andamiaje MusicXML para esta situación."
    )

    raw_text = query_ai_model(system_prompt, user_prompt)

    # Extraer bloque XML si la IA añade texto extra
    xml_start = raw_text.find("<?xml")
    xml_end = raw_text.rfind("</score-partwise>") + len("</score-partwise>")

    if xml_start != -1 and xml_end > xml_start:
        return raw_text[xml_start:xml_end]
    return raw_text  # devuelve todo si no detecta etiquetas


def save_musicxml_file(xml_content, filename="output_scaffold.musicxml"):
    """Guarda el resultado en un archivo."""
    if xml_content:
        with open(filename, "w") as file:
            file.write(xml_content)
        print(f"✅ ¡Éxito! Andamiaje musical generado en: {filename}")
        print("Arrastra este archivo a MuseScore para verlo.")
    else:
        print("❌ No se pudo generar el archivo MusicXML.")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    print("--- N2N BRIDGE INICIADO (Groq) ---")

    telemetry = read_game_telemetry("telemetry.json")
    print(f"Datos del juego leídos: {telemetry['musical_request']['target_emotion']}")

    xml_result = generate_musicxml_scaffold(telemetry)
    save_musicxml_file(xml_result)
