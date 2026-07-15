"""
Adaptive Music Engine — FastAPI entry point
"""

import sys
import os

# Allow local imports from this directory
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import AdaptiveMusicRequest, AdaptiveMusicResponse, TelemetryData, N2NMusicalRequest
from music_engine import generate_music_profile
from bridge import N2NBridge

import time
import logging

logger = logging.getLogger(__name__)
bridge = N2NBridge()

app = FastAPI(
    title="Adaptive Music Engine",
    description=(
        "Recibe el estado del juego en JSON y devuelve parámetros musicales adaptativos: "
        "tempo, tonalidad, capas de instrumentos, efectos y parámetros de mezcla."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "Adaptive Music Engine",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoint": "POST /music/generate",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/music/generate", response_model=AdaptiveMusicResponse)
def generate_music(request: AdaptiveMusicRequest) -> AdaptiveMusicResponse:
    """
    Genera un perfil musical adaptativo a partir del estado del juego.

    Ejemplo de entrada:
    ```json
    {
      "game_state": {
        "player_health": 25,
        "enemy_proximity": "close",
        "environment": "dark_cave",
        "narrative_tension_level": 8,
        "is_in_combat": true
      },
      "musical_request": {
        "transition_type": "abrupt",
        "target_emotion": "urgent_survival"
      }
    }
    ```
    """
    try:
        return generate_music_profile(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/music/generate-ai")
def generate_music_ai(request: AdaptiveMusicRequest):
    """
    Versión enriquecida con Gemini: genera el perfil musical por reglas y luego
    añade análisis narrativo, sugerencias de composición y variaciones dinámicas.

    Requiere el secreto `IA_API_KEY` configurado en el entorno.
    """
    try:
        base_response = generate_music_profile(request)
        profile_dict = base_response.music_profile.model_dump()
        state_dict = request.game_state.model_dump()

        from gemini_advisor import enrich_music_profile
        enrichment = enrich_music_profile(state_dict, profile_dict)

        return {
            **base_response.model_dump(),
            "ai_enrichment": enrichment,
        }
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/generate")
async def generate_musicxml(telemetry: TelemetryData):
    """
    Endpoint N2N Bridge: recibe telemetría y devuelve MusicXML generado por IA (Groq).

    Ejemplo de entrada:
    ```json
    {
      "player_health": 25,
      "enemy_proximity": 90,
      "environment": "dark_cave",
      "narrative_tension_level": 8,
      "is_in_combat": true,
      "musical_request": {
        "emotions": ["tenso", "urgente", "misterioso"]
      }
    }
    ```
    """
    try:
        telemetry_dict = telemetry.dict()
        xml_content = bridge.generate_musicxml(telemetry_dict)
        filename = f"output_{int(time.time())}.musicxml"
        bridge.save_musicxml(xml_content, filename)
        return {
            "status": "success",
            "filename": filename,
            "musicxml": xml_content,
        }
    except Exception as e:
        logger.error(f"Error interno: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/music/environments")
def list_environments():
    """Lista todos los ambientes disponibles."""
    from models import Environment
    return {"environments": list(Environment.__args__)}


@app.get("/music/emotions")
def list_emotions():
    """Lista todas las emociones objetivo disponibles."""
    from models import TargetEmotion
    return {"emotions": list(TargetEmotion.__args__)}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
