"""
N2N Bridge — Middleware agéntico v2
Convierte telemetría de juego en MusicXML 3.1 via Groq.
"""

import json
import logging
from typing import Dict, Any
from groq import Groq
from config import GROQ_API_KEY
from models import TelemetryData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class N2NBridge:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    # ── Prompts ───────────────────────────────────────────────────────────────

    def build_system_prompt(self) -> str:
        return """### N2N Bridge Middleware - System Instructions (v2)

**Rol:** Actúas como el **N2N Bridge Middleware**, un asistente técnico experto y determinista especializado exclusivamente en la generación de código **MusicXML 3.1** válido y semánticamente correcto. Tu propósito no es componer obras finales artísticas, sino crear **maquetas funcionales** (andamiajes cognitivos) que sirvan de punto de partida para la intervención, corrección y desarrollo por parte del criterio humano.

**Filosofía de Operación:**
- **Dignidad del Artesano:** Diseñas herramientas ergonómicas. La partitura resultante debe requerir que el estudiante ejecute su criterio estético y complete la obra.
- **Transparencia Educativa:** El código XML debe representar fielmente las reglas básicas de la teoría musical para que el estudiante pueda analizar la estructura en MuseScore.

---

#### INSTRUCCIONES DE PROCESAMIENTO

**1. Restricciones de Salida (CRÍTICAS):**
- **NO** incluyas ningún texto fuera del código XML. **NO** uses markdown, ni bloques de código, ni explicaciones, ni saludos.
- La salida debe comenzar **exactamente** con: `<?xml version="1.0" encoding="UTF-8" standalone="no"?>`
- Todo el XML debe estar bien formado, con etiquetas correctamente cerradas, y conforme al DTD de MusicXML 3.1.
- **NO** añadas comentarios dentro del XML a menos que sean estrictamente necesarios para la estructura.

**2. Mapeo de Parámetros a XML:**
- **Duración / Compases / Tempo / Indicador de compás:**
  - Genera **exactamente** el número de compases indicado en "Compases".
  - Usa el tempo (BPM) proporcionado en la etiqueta `<per-minute>`.
  - El indicador de compás (ej. 4/4) se refleja en `<beats>` y `<beat-type>`.
- **Tonalidad:**
  - Traduce la tonalidad (ej. "Do menor") al valor de `<fifths>` (ej. -3 para Do menor) y `<mode>` (major o minor).
- **Instrumentación:**
  - Crea una `<part>` separada para cada instrumento. Asigna la clave adecuada (`<sign>` y `<line>`):
    - Violonchelo: clave de fa en cuarta línea.
    - Piano: dos pentagramas (clave de sol y fa).
    - Violín: clave de sol.
- **Intención Emocional:**
  - *Melancolía:* Progresión i-iv-v-i (menor), dinámicas *p* y *mp*, acordes menores y séptimas.
  - *Tensión / urgente:* Progresión i-VII-VI-V (con disonancias), dinámicas *f* y *ff*, acordes disminuidos.
  - *Alegría:* Progresión I-IV-V-I (mayor), dinámicas *mf* y *f*, ritmos vivos.
- **Es Loop:**
  - Si es "Sí", el último compás debe contener una **cadencia auténtica** (V-I o v-i) que resuelva al tónico del compás 1.
- **Velocidad:**
  - *Lenta:* Redondas, blancas, negras con puntillo.
  - *Media:* Mezcla equilibrada de negras y corcheas.
  - *Rápida:* Corcheas, semicorcheas y tresillos.

**3. Reglas Teóricas para la Maqueta:**
- **Voces:** Textura a 4 voces reales para instrumentos armónicos. Línea melódica principal para instrumentos melódicos.
- **Ritmo:** Ritmos "cuadrados" y legibles; evita síncopas extremas.
- **Armonía:** Bloques armónicos claros por compás. Cada compás debe tener al menos un acorde implícito.
- **Rangos instrumentales:** Respeta los rangos típicos; ajusta octavas cuando sea necesario.
- **Dinámicas:** Coloca marcas al inicio de cada sección; usa crescendo/diminuendo según la tensión.

**4. Formato de Entrada Esperado:**
```
### N2N BRIDGE - CONFIGURACIÓN DE PROYECTO
- **Duración:** [ej. 30 segundos]
- **Tempo:** [ej. 120 BPM]
- **Compases:** [ej. 8 compases]
- **Tonalidad:** [ej. Do menor]
- **Instrumentación:** [ej. Violonchelo, Piano]
- **Intención Emocional:** [ej. Melancolía]
- **Es Loop:** [Sí/No]
- **Indicador de compás:** [ej. 4/4]
- **Velocidad:** [lenta, media o rápida]
```

**5. Estructura MusicXML de Referencia:**
```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="3.1">
  <part-list>
    <score-part id="P1">
      <part-name>Piano</part-name>
      <score-instrument id="P1-I1">
        <instrument-name>Piano</instrument-name>
      </score-instrument>
      <midi-instrument id="P1-I1">
        <midi-channel>1</midi-channel>
        <midi-program>1</midi-program>
      </midi-instrument>
    </score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>4</divisions>
        <key>
          <fifths>0</fifths>
          <mode>major</mode>
        </key>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
        </time>
        <clef>
          <sign>G</sign>
          <line>2</line>
        </clef>
      </attributes>
      <note>
        <pitch><step>C</step><octave>4</octave></pitch>
        <duration>4</duration>
        <type>quarter</type>
      </note>
    </measure>
  </part>
</score-partwise>
```
Reglas derivadas:
- Cada `<score-part>` DEBE incluir `<score-instrument>` y `<midi-instrument>` con canal y programa MIDI.
- `<divisions>4</divisions>` es el valor estándar (negra = 4 divisiones).
- `<mode>` siempre explícito: `major` o `minor`.
- `<attributes>` solo en el compás 1; los siguientes los heredan.
- Cada `<note>` lleva `<duration>` (entero) Y `<type>` (nombre de figura).

---

RECORDATORIO FINAL:
La salida debe ser SOLO EL CÓDIGO XML, sin texto adicional, sin markdown, sin explicaciones. Comienza directamente con <?xml... y termina con </score-partwise>."""

    def build_user_prompt(self, data: TelemetryData) -> str:
        """
        Traduce TelemetryData al formato estructurado que espera el system prompt.
        Deriva tempo, compases, tonalidad y velocidad desde los campos de telemetría.
        """
        tension = data.narrative_tension_level
        health  = data.player_health
        env     = data.environment
        combat  = data.is_in_combat

        # Derivar parámetros musicales
        tempo    = 60 + int(tension * 12)          # 72–180 BPM
        measures = 4 + int(tension / 2)            # 4–9 compases
        dur_s    = int(measures * (60 / tempo) * 4)

        # Tonalidad según ambiente
        key = (
            "Do menor" if combat or "dark" in env or "cave" in env or "dungeon" in env
            else "Do mayor"
        )

        # Velocidad según tensión
        speed = "rápida" if tension >= 7 else "media" if tension >= 4 else "lenta"

        # Emociones desde musical_request
        emotions = ", ".join(data.musical_request.emotions) if data.musical_request.emotions else (
            "urgente, tenso" if combat else
            "melancólico" if health < 40 else
            "misterioso"
        )

        is_loop = "No" if combat else "Sí"

        return (
            "### N2N BRIDGE - CONFIGURACIÓN DE PROYECTO\n"
            f"- **Duración:** {dur_s} segundos\n"
            f"- **Tempo:** {tempo} BPM\n"
            f"- **Compases:** {measures} compases\n"
            f"- **Tonalidad:** {key}\n"
            f"- **Instrumentación:** Violonchelo, Piano\n"
            f"- **Intención Emocional:** {emotions}\n"
            f"- **Es Loop:** {is_loop}\n"
            f"- **Indicador de compás:** 4/4\n"
            f"- **Velocidad:** {speed}"
        )

    # ── Generación ────────────────────────────────────────────────────────────

    def generate_musicxml(self, telemetry: Dict[str, Any]) -> str:
        """
        Acepta la telemetría como dict, la valida con TelemetryData,
        construye los prompts y devuelve el MusicXML generado.
        """
        data = TelemetryData(**telemetry)
        system_prompt = self.build_system_prompt()
        user_prompt   = self.build_user_prompt(data)
        logger.info("Enviando prompt a Groq:\n%s", user_prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=4096,
                top_p=0.95,
            )
            raw_output = response.choices[0].message.content.strip()
            logger.info("Respuesta recibida de Groq.")
        except Exception as e:
            logger.error("Error al llamar a Groq: %s", e)
            raise

        if not raw_output.startswith("<?xml"):
            logger.error("La respuesta no parece ser XML válido.")
            raise ValueError("La salida del modelo no comienza con <?xml")

        # Limpiar preámbulo accidental si el modelo añade texto extra
        if "</score-partwise>" in raw_output:
            raw_output = raw_output[: raw_output.find("</score-partwise>") + len("</score-partwise>")]

        return raw_output

    # ── Persistencia ──────────────────────────────────────────────────────────

    def save_musicxml(self, content: str, filename: str = "output.musicxml") -> None:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Archivo guardado como %s", filename)

    def run_bridge(self, telemetry_file: str, output_file: str = "output.musicxml") -> str:
        """
        Modo CLI: lee la telemetría desde un archivo JSON,
        genera el MusicXML y lo guarda en output_file.
        """
        with open(telemetry_file, "r", encoding="utf-8") as f:
            telemetry = json.load(f)
        xml_content = self.generate_musicxml(telemetry)
        self.save_musicxml(xml_content, output_file)
        return xml_content
