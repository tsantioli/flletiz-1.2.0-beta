# 🤖 Fletiz — Asistente de IA con Control del Sistema

Fletiz es un chatbot desktop moderno construido con **Flet**, **Groq** y **Tool Use**. Permite comunicación por texto y voz, con capacidad de interactuar con el sistema operativo (abrir archivos, leer contenidos, buscar rutas).

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [Componentes](#componentes)
- [Tool Use](#tool-use)
- [Roadmap](#roadmap)
- [Contribución](#contribución)

---

## ✨ Características

### Implementadas ✅
- **Interfaz moderna** — UI oscura con paleta dorado/naranja/negro
- **Chat bidireccional** — Burbujas de mensaje con alineación por autor
- **Historial de conversación** — Contexto persistente en sesión
- **Entrada por voz** — Reconocimiento de voz con `speech_recognition`
- **Tool Use avanzado** — El bot puede ejecutar acciones en tu sistema
  - Abrir archivos y programas
  - Leer contenido de archivos
  - Buscar rutas de programas instalados
- **Threading** — La interfaz no se congela mientras espera respuestas
- **API Key segura** — Variables de entorno con `.env`
- **Validación de entrada** — No envía mensajes vacíos

### En desarrollo 🔄
- Persistencia en PostgreSQL
- Más herramientas (escribir archivos, listar carpetas)
- Indicador de "escribiendo..."
- Confirmación de acciones del bot

### Planificado 🎯
- Integración con calendarios
- Análisis de archivos (PDF, Excel)
- Multi-lenguaje
- Temas personalizables
- Historial sincronizado en cloud

---

## 📦 Requisitos

- **Python 3.8+**
- **PostgreSQL 15+** (opcional, para persistencia)
- **Micrófono** (opcional, para entrada de voz)
- **Sistema Operativo**: Windows, macOS, Linux

### Dependencias Python
```
flet==0.23.1
groq==0.10.0
python-dotenv==1.0.0
SpeechRecognition==3.10.0
pyttsx3==2.90
psycopg2-binary==2.9.9
```

---

## 🚀 Instalación

### 1. Clonar o descargar el proyecto
```bash
cd tu_carpeta_de_proyectos
# Descarga los archivos de Fletiz
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Crear archivo `.env`
En la raíz del proyecto, crea `.env`:
```
GROQ=tu_api_key_groq_aqui
```

**Obtener API Key:**
- Ve a [console.groq.com](https://console.groq.com)
- Crea una cuenta gratis
- Genera una API Key en la sección API Keys
- Cópiala a `.env`

### 5. Ejecutar
```bash
python main.py
```

---

## ⚙️ Configuración

### Variables de entorno (`.env`)
```env
GROQ=gsk_xxxxxxxxxxxxx  # Tu API Key de Groq
```

### Personalización del bot (`config.py`)
Edita `SYSTEM_PROMPT` para cambiar:
- Nombre del bot
- Personalidad
- Instrucciones especiales
- Idioma

Ejemplo:
```python
SYSTEM_PROMPT = """
Eres Fletiz, un asistente especializado en programación.
Hablas español con emojis.
Siempre explicas conceptos de forma sencilla.
"""
```

---

## 🎮 Uso

### Interfaz Principal
```
┌─────────────────────────────────┐
│     Mi Chatbot ✨               │
├─────────────────────────────────┤
│ [Chat area - burbujas]          │
│                                 │
│ Tú: Hola, ¿cómo estás?         │
│ Bot: ¡Hola! Estoy bien 😊      │
├─────────────────────────────────┤
│ [Input field] [Enviar] [🎤]    │
└─────────────────────────────────┘
```

### Controles
- **Escribir**: Campo de texto
- **Enviar**: Enter o botón "Enviar"
- **Voz**: Botón 🎤 (habla y se escribe automáticamente)

### Ejemplos de interacción
```
Usuario: "Abre el bloc de notas"
Bot: Abriendo bloc de notas...
[Se abre notepad.exe]

Usuario: "Lee el archivo config.py"
Bot: Leyendo el archivo...
[Lee y muestra el contenido]

Usuario: "¿Dónde está Python?"
Bot: Python se encuentra en: C:\Program Files\Python313
```

---

## 🏗️ Arquitectura

### Diagrama de flujo
```
Usuario input (texto/voz)
    ↓
send_message()
    ↓
Valida mensaje (no vacío)
    ↓
Limpia entrada UI
    ↓
Threading → procesar()
    ↓
Llamada a Groq API
    ↓
¿Tool Call?
├─ Sí → Ejecutar herramienta
│       └─ resultado
└─ No → Respuesta de texto
    ↓
Agregar al historial
    ↓
Mostrar burbujas
    ↓
chat.update()
```

### Stack tecnológico
| Componente | Tecnología | Propósito |
|-----------|-----------|----------|
| UI | Flet | Interfaz gráfica multi-plataforma |
| LLM | Groq (Llama 3.3) | Procesamiento de lenguaje |
| Voz | SpeechRecognition + pyttsx3 | Entrada/salida de audio |
| Async | Threading | No bloquear interfaz |
| Config | python-dotenv | Variables de entorno |
| BD | PostgreSQL | Persistencia (futuro) |

---

## 🔧 Componentes

### `main.py`
**Archivo principal** — Interfaz y lógica de chat
- Función `main(page)` — Inicializa UI con Flet
- Función `send_message(e)` — Procesa envío de mensajes
- Función `crear_burbuja()` — Renderiza mensajes
- Función `activar_voz()` — Activa reconocimiento de voz
- Función `agregar_al_historial()` — Gestiona contexto

**Dependencias internas**: `config.py`, `tools.py`, `voz.py`

```python
# Ejemplo de extensión
def send_message(e):
    mensaje = entrada.value
    if not mensaje.strip():
        return
    
    entrada.value = ""
    page.update()
    
    def procesar():
        # Tu código aquí
        respuesta = client.chat.completions.create(...)
        # ...
    
    threading.Thread(target=procesar, daemon=True).start()
```

### `config.py`
**Configuración centralizada**
- `SYSTEM_PROMPT` — Personalidad e instrucciones del bot

```python
SYSTEM_PROMPT = """
Eres Fletiz...
"""
```

### `tools.py`
**Herramientas del sistema** — Permite que el bot interactúe con tu PC

**Funciones:**
- `abrir_archivo(nombre)` — Abre programas/archivos
- `leer_archivo(nombre)` — Lee contenido de archivos
- `buscar_ruta(nombre)` — Busca ubicación de programas

**Variable:**
- `TOOLS` — Definición de herramientas en formato Groq

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "abrir_archivo",
            "description": "Abre un archivo o programa",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre del archivo a abrir"
                    }
                },
                "required": ["nombre"]
            }
        }
    },
    # ... más herramientas
]
```

### `voz.py`
**Reconocimiento y síntesis de voz**

**Funciones:**
- `escuchar()` — Captura audio del micrófono y convierte a texto
- `hablar(texto)` — Lee texto en voz alta (no usado actualmente)

```python
def escuchar():
    r = sr.Recognizer()
    text = ""
    try:
        with sr.Microphone() as source:
            audio = r.listen(source)
        text = r.recognize_google(audio, language="es-ES").upper()
    except sr.UnknownValueError:
        print("No se pudo entender el audio")
    return text
```

### `database.py` (Planificado)
**Gestión de base de datos PostgreSQL**
- Guardar/recuperar historial
- Crear tabla de conversaciones
- Consultas de contexto histórico

---

## 🛠️ Tool Use

### ¿Qué es?
Tool Use permite que Groq **decida cuándo usar herramientas** basado en el contexto. No es un simple if/else, es inteligencia artificial decidiendo qué hacer.

### Flujo
```
Usuario: "Abre Spotify"
    ↓
Groq recibe: SYSTEM_PROMPT + historial + TOOLS
    ↓
Groq decide: "Necesito usar 'abrir_archivo' con parámetro 'Spotify'"
    ↓
Respuesta llega con finish_reason="tool_calls"
    ↓
Extraemos tool_name y tool_args
    ↓
Ejecutamos: abrir_archivo(tool_args["nombre"])
    ↓
Resultado se agrega al historial
    ↓
Bot responde: "Abriendo Spotify para ti 🎵"
```

### Código técnico
```python
if respuesta.choices[0].finish_reason == "tool_calls":
    tool_call = respuesta.choices[0].message.tool_calls[0]
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    
    if tool_name == "abrir_archivo":
        resultado = abrir_archivo(tool_args["nombre"])
    elif tool_name == "leer_archivo":
        resultado = leer_archivo(tool_args["nombre"])
    elif tool_name == "buscar_ruta":
        resultado = buscar_ruta(tool_args["nombre"])
```

### Agregar nueva herramienta
1. Crea función en `tools.py`
2. Agrega definición a `TOOLS` con descripción y parámetros
3. Agrega case en `send_message()`

Ejemplo:
```python
# 1. Nueva función
def escribir_archivo(ruta, contenido):
    try:
        with open(ruta, 'w') as f:
            f.write(contenido)
        return f"Archivo creado en {ruta}"
    except Exception as e:
        return f"Error: {e}"

# 2. Agregar a TOOLS
{
    "type": "function",
    "function": {
        "name": "escribir_archivo",
        "description": "Escribe contenido en un archivo",
        "parameters": {
            "type": "object",
            "properties": {
                "ruta": {"type": "string"},
                "contenido": {"type": "string"}
            },
            "required": ["ruta", "contenido"]
        }
    }
}

# 3. Agregar case
elif tool_name == "escribir_archivo":
    resultado = escribir_archivo(
        tool_args["ruta"],
        tool_args["contenido"]
    )
```

---

## 🛣️ Roadmap

### Q1 2026
- [ ] PostgreSQL persistencia
- [ ] Indicador "escribiendo..."
- [ ] Confirmación de acciones peligrosas
- [ ] Caché de respuestas

### Q2 2026
- [ ] Integración con Google Calendar
- [ ] Procesamiento de PDFs
- [ ] Multi-usuario (login)
- [ ] Sincronización en cloud

### Q3 2026
- [ ] Modelo custom fine-tuned
- [ ] Plugins de terceros
- [ ] API REST pública
- [ ] Móvil (Flutter)

---

## 🤝 Contribución

### Cómo contribuir
1. Fork del proyecto
2. Crea rama: `git checkout -b feature/mi-feature`
3. Commit: `git commit -m "Agrego mi feature"`
4. Push: `git push origin feature/mi-feature`
5. Pull Request

### Estándares de código
- Python 3.8+ syntax
- PEP 8 style guide
- Docstrings en funciones
- Manejo de excepciones

### Reportar bugs
- Título descriptivo
- Pasos para reproducir
- Resultado esperado vs actual
- Sistema operativo y versión Python

### Sugerencias de features
- Descripción clara del caso de uso
- Ejemplo de cómo se usaría
- Impacto en arquitectura

---

## 📝 Licencia

Fletiz está bajo licencia MIT. Libre para uso personal y comercial.

---

## 👨‍💻 Autores

- **Desarrollador Principal**: TOMAS SANTIAGO OLIVAR RIVAS  
- **Contribuidores**: [Agregar equipo]

---




- **Email**: tsantiolivar@gmail.com



---

## 🎓 Aprende más

- [Flet Documentation](https://flet.dev)
- [Groq API Docs](https://console.groq.com/docs)
- [Tool Use Guide](https://console.groq.com/docs/tool-use)
- [Speech Recognition](https://github.com/Uberi/speech_recognition)

---

**Hecho con ❤️ y ☕**