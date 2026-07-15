```markdown
# N2N Bridge Middleware

**N2N Bridge** es un middleware inteligente que convierte telemetría de videojuegos en partituras **MusicXML 3.1** utilizando IA (Groq). El sistema actúa como un puente entre el estado del juego y la notación musical, generando **andamiajes estructurales** (scaffolding) que sirven como punto de partida para compositores humanos.

---

## 🎯 Características

- **Traducción semántica**: Convierte variables de juego (tensión, entorno, combate) en parámetros musicales (armonía, ritmo, dinámica, instrumentación).
- **MusicXML 3.1**: Genera código válido y bien formado, compatible con MuseScore 4 y otros software de notación.
- **API REST**: Expone endpoints para recibir telemetría y devolver partituras.
- **Andamiaje estructural**: Crea maquetas funcionales con 4 voces reales, progresiones armónicas lógicas y respeto por los rangos instrumentales.
- **Determinista y educativo**: Diseñado para que el compositor humano complete y refine la obra.

---

## 🚀 Tecnologías

- **Python 3.10+**
- **FastAPI** - Framework web para la API REST
- **Groq SDK** - Conexión con el modelo Llama 3.3 70B
- **Pydantic** - Validación de datos de telemetría
- **Uvicorn** - Servidor ASGI

---

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/N2N_Bridge_Final.git
cd N2N_Bridge_Final
```

2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto:

```env
GROQ_API_KEY=tu_clave_aqui
```

---

🖥️ Uso

Ejecutar el servidor

```bash
python main.py
```

El servidor estará disponible en http://localhost:8000.

Endpoints disponibles

POST /generate

Recibe telemetría y genera un archivo MusicXML.

Ejemplo de petición:

```json
{
  "player_health": 45.0,
  "enemy_proximity": 78.0,
  "environment": "dark_cave",
  "narrative_tension_level": 8,
  "is_in_combat": true,
  "musical_request": {
    "emotions": ["tenso", "oscuro", "urgente"]
  }
}
```

Respuesta:

```json
{
  "status": "success",
  "filename": "output_1702345678.musicxml",
  "musicxml": "<?xml version=\"1.0\" ... </score-partwise>"
}
```

GET /health

Verifica que el servicio esté activo.

---

📁 Estructura del Proyecto

```
N2N_Bridge_Final/
├── main.py              # Servidor FastAPI
├── bridge.py            # Lógica principal (conexión con Groq)
├── models.py            # Modelos Pydantic para telemetría
├── config.py            # Configuración y variables de entorno
├── requirements.txt     # Dependencias
├── telemetry_example.json # Ejemplo de telemetría para pruebas
└── README.md            # Este archivo
```

---

🎼 ¿Cómo funciona internamente?

1. El usuario envía telemetría al endpoint /generate.
2. El sistema construye un prompt con instrucciones específicas para el LLM (rol, restricciones, reglas teóricas, mapeo de parámetros).
3. Groq procesa el prompt y genera código MusicXML 3.1 limpio, sin texto adicional.
4. El archivo se guarda con un timestamp único en el servidor.
5. La partitura puede abrirse en MuseScore para revisión y edición.

---

🧪 Pruebas rápidas

Con curl

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @telemetry_example.json
```

Con Python (requests)

```python
import requests
import json

telemetry = {
    "player_health": 45.0,
    "enemy_proximity": 78.0,
    "environment": "dark_cave",
    "narrative_tension_level": 8,
    "is_in_combat": True,
    "musical_request": {
        "emotions": ["tenso", "oscuro"]
    }
}

response = requests.post("http://localhost:8000/generate", json=telemetry)
print(response.json())
```

---

🔧 Personalización

Modificar el prompt del sistema

Edita bridge.py en el método build_system_prompt(). Puedes ajustar:

· Reglas de armonía y contrapunto.
· Rangos instrumentales.
· Mapeo de emociones a progresiones armónicas.
· Parámetros de densidad rítmica.

Cambiar el modelo de Groq

En bridge.py, modifica:

```python
self.model = "llama-3.3-70b-versatile"  # Cambia por otro modelo disponible
```

Ajustar parámetros de generación

En generate_musicxml(), modifica:

```python
temperature=0.7,      # Creatividad (0-1)
max_tokens=4096,      # Límite de longitud
top_p=0.95            # Muestreo de núcleo
```

---

📚 Dependencias principales

Paquete Versión Uso
fastapi 0.115.6 Framework web
uvicorn 0.34.0 Servidor ASGI
groq 0.10.0 SDK para Groq API
python-dotenv 1.0.1 Carga de variables de entorno
pydantic 2.9.2 Validación de datos

---

🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerir mejoras.

---

📄 Licencia

MIT License - ver archivo LICENSE para más detalles.

---

👤 Autor

Sergio Andrés Gutiérrez León

· GitHub: @sergioandresgutierrezleon-lab

---

🙏 Agradecimientos

· Groq por proporcionar el modelo Llama 3.3 70B.
· MuseScore por su excelente software de notación musical.
· Comunidad de código abierto por las herramientas que hacen posible este proyecto.

---

Nota: Este sistema está diseñado para generar andamiajes estructurales, no obras finalizadas. La intención es acelerar el flujo de trabajo del compositor, no reemplazar su criterio artístico.

```
