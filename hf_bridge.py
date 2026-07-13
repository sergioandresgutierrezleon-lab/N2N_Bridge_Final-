# N2N Bridge (Note-to-Note)
# Agentic AI Middleware for Adaptive Music Scores via MusicXML
# Built for the Kanz AI Hackathon

import os
import json
from groq import Groq

# --- CONFIGURACIÓN ---
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("ERROR: La clave GROQ_API_KEY no se encontró en el entorno.")

groq_client = Groq(api_key=api_key)

# Nombres de los archivos
INPUT_FILE = 'telemetry.json'
OUTPUT_FILE = 'output_scaffold.musicxml'

# --- MASTER SYSTEM PROMPT (LA TESIS INTEGRADA) ---
# Este prompt avanzado define la personalidad, las reglas estrictas de
# orquestación y el formato de salida para el Agente orquestador.
agentic_prompt = """
### ROLE AND MISSION
You are an expert Musicologist and Orchestrator Agent. Your mission is to ingest raw game telemetry data and generate a structured, professional-grade musical scaffolding as a deterministic MusicXML 3.1 file. You provide "Cognitive Scaffolding," allowing a human composer to finalize the aesthetic work.

### COMPOSITION AND ORCHESTRATION RULES (STRICT)

1. OUTPUT FORMAT: Generate ONLY a valid, parseable MusicXML 3.1 string.
2. NO CHAT: Do not include introductory text, explanations, or code block formatting (like ```xml). Start immediately with "<?xml version...".
3. DETERMINISTIC MAPPING (Telemetry to Music):
   - game_state.narrative_tension_level (1-10): Maps to rhythmic density (higher=more notes) and dissonance.
   - game_state.environment: Maps to harmonic complexity and instrumentation texture. E.g., 'dark_cave' = harmonic minor or octatonic, low brass/woodwinds. 'open_field' = diatonic/major, strings/woodwinds.
   - game_state.is_in_combat (bool): If true, add ostinatos and complex percussion patterns.
   - game_state.requested_orchestration_staves: If provided, prioritize creating specific parts/staves for these standard orchestral sections.
   - musical_request.target_emotion: Overrides overall tone (e.g., 'urgent_survival' forces high tempo and tense orchestration).
4. HARMONIC ANALYSIS: Do not just provide melody lines. Provide full four-part or larger orchestral scaffolding. Analyze the implied harmony based on the environment and tension, and write the appropriate XML nodes for chords, voice leading, and dynamic markings.
5. INSTRUMENTATION: Map choices to standard orchestral families (Woodwinds, Brass, Percussion, Strings). Each choice must be justified by the input telemetry in your reasoning.
6. NO PLAGIARISM: Create original, rule-based compositional patterns, not copyrighted motifs.

### GUIDING PRINCIPLE
Create a functional, playable, and complex orchestral sketch that is intellectually challenging for a human composer to receive.
"""

# --- FUNCIÓN PRINCIPAL ---
def generate_musicxml_scaffold():
    print("--- INICIANDO N2N BRIDGE ---")
    print(f"Leyendo telemetría de: {INPUT_FILE}...")

    # 1. Leer los datos de telemetría del juego
    try:
        with open(INPUT_FILE, 'r') as file:
            telemetry_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo {INPUT_FILE} no se encontró.")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo {INPUT_FILE} no es un JSON válido.")
        return

    print("Telemetría leída con éxito.")
    print("Llamando a la API de Groq (Llama 3.3 70B)...")

    # 2. Llamada a la API de Groq con el Master System Prompt
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                # MENSAJE DE SISTEMA: Define la personalidad y reglas avanzadas
                {
                    "role": "system",
                    "content": agentic_prompt
                },
                # MENSAJE DE USUARIO: Provee los datos dinámicos del juego
                {
                    "role": "user",
                    "content": f"Generate the expert MusicXML sketch for this game state: {json.dumps(telemetry_data, indent=2)}"
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,  # Baja temperatura para máxima consistencia técnica.
        )
    except Exception as e:
        print(f"Error durante la llamada a la API: {e}")
        return

    # 3. Extraer el contenido del MusicXML
    musicxml_content = chat_completion.choices[0].message.content.strip()

    # Limpieza de seguridad: eliminar cualquier preámbulo si el LLM falló las reglas.
    if "<?xml" in musicxml_content:
        start_index = musicxml_content.find("<?xml")
        musicxml_content = musicxml_content[start_index:]
        if "</score-partwise>" in musicxml_content:
            end_index = musicxml_content.find("</score-partwise>") + len("</score-partwise>")
            musicxml_content = musicxml_content[:end_index]

    # 4. Guardar el resultado en el archivo .musicxml
    print(f"Guardando partitura compleja en: {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as file:
        file.write(musicxml_content)

    print("--- PROCESO COMPLETADO ---")
    print(f"Ahora puedes abrir '{OUTPUT_FILE}' en MuseScore 4 para ver y escuchar la orquestación agéntica avanzada.")

# Ejecutar la función principal
if __name__ == "__main__":
    generate_musicxml_scaffold()
