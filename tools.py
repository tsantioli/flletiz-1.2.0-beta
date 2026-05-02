import os
import subprocess
from os import startfile, makedirs
from shutil import which
import pyautogui as pya
import time

def abrir_archivo(nombre):
    try:
        startfile(nombre)
    except Exception as e:
        return f"Error al abrir el archivo: {e}"

def leer_archivo(nombre):
    try:
        with open(nombre, 'r') as archivo:
            return archivo.read()
    except Exception as e:
        return f"Error al leer el archivo: {e}"

def buscar_ruta(nombre):
    try:
        return which(nombre)
    except Exception as e:
        return f"Error al buscar la ruta: {e}"

def listar_archivos(ruta="."):
    try:
        archivos = os.listdir(ruta)
        return f"Archivos en {os.path.abspath(ruta)}: {', '.join(archivos)}"
    except Exception as e:
        return f"Error al listar archivos: {e}"

def escribir_vscode(codigo, nombre_archivo="codigo.py"):
    try:
        # 1. Verificación básica de sintaxis solo si es Python
        if nombre_archivo.endswith(".py"):
            try:
                compile(codigo, '<string>', 'exec')
            except (IndentationError, SyntaxError) as e:
                return f"Error de indentación/sintaxis en el código Python: {e}\nCódigo rechazado."
        
        # 2. Preparar el directorio y la ruta
        directorio = "fletiza"
        if not os.path.exists(directorio):
            makedirs(directorio)
            
        if not nombre_archivo:
            nombre_archivo = "codigo.py"
        ruta_archivo = os.path.join(directorio, nombre_archivo)

        # 3. Escribir el archivo físicamente (mucho más rápido y seguro)
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(codigo)

        # 4. Abrir VS Code directamente en el archivo usando subprocess
        # Esto asume que 'code' está en el PATH del sistema
        subprocess.run(["code", os.path.abspath(ruta_archivo)], shell=True)

        return f"Éxito: Archivo creado en {ruta_archivo} y abierto en VS Code."
    except Exception as e:
        return f"Error al procesar el archivo: {e}"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "abrir_archivo",
            "description": "Abre un programa, aplicación o archivo en el sistema. Úsalo cuando el usuario pida 'abrir' algo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre del ejecutable (ej: 'spotify', 'chrome') o ruta del archivo."
                    }
                },
                "required": ["nombre"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "leer_archivo",
            "description": "Lee y devuelve el contenido de texto de un archivo específico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Ruta completa o nombre del archivo a leer."
                    }
                },
                "required": ["nombre"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_ruta",
            "description": "Busca en el PATH del sistema la ubicación de un ejecutable.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre del comando o programa a localizar."
                    }
                },
                "required": ["nombre"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_archivos",
            "description": "Lista los archivos en un directorio. Útil para conocer el contexto antes de leer o escribir archivos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ruta": {
                        "type": "string",
                        "description": "Ruta del directorio (por defecto el actual '.')."
                    }
                }
            }
        }
    },
     {
        "type": "function",
        "function": {
            "name": "escribir_vscode",
            "description": "Crea un nuevo archivo de código y lo abre en Visual Studio Code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {
                        "type": "string",
                        "description": "El contenido completo del archivo."
                    },
                    "nombre_archivo": {
                        "type": "string",
                        "description": "Nombre del archivo con extensión (ej: 'app.py', 'index.html')."
                    }
                },
                "required": ["codigo"]
            }
        }
    } 

]
