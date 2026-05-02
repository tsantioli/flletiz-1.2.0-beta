import flet as ft
from tools import *
import json 
from groq import Groq
from config import SYSTEM_PROMPT    
from voz import escuchar
import threading
import os 
from dotenv import load_dotenv
import pyautogui
import time
# Obtener la ruta absoluta de la carpeta donde está este script
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

API_KEY = os.getenv("GROQ")
if not API_KEY:
    print("Error: No se encontró la variable 'GROQ' en el archivo .env o en el sistema.")
client = Groq(api_key=API_KEY)


def main(page: ft.Page):
    page.title = "chatbot"
    page.vertical_alignment = "center"
    page.bgcolor ="#0a0a0a"
    
    chat = ft.ListView(
        padding=20,
        auto_scroll=True,
        expand=True,
        spacing=10,
    )
    entrada = ft.TextField(
        hint_text="Escribe tu mensaje",
        expand=True,
        on_submit=lambda e: send_message(e)
    )    

    def send_message(e):
        mensaje = entrada.value
        if not mensaje.strip():
            return

        entrada.value = ""
        page.update()
        
        def procesar():
            respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content":SYSTEM_PROMPT}, *historial, {"role": "user", "content": mensaje}],
            tools = TOOLS)

            odtencuin = respuesta.choices[0].message.content
            
            try:
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
                    elif tool_name == "escribir_vscode":
                        resultado = escribir_vscode(tool_args["codigo"])
                else:
                    odtencuin = respuesta.choices[0].message.content
            except Exception as e:
                odtencuin = f"Error al procesar la respuesta: {e}"
            
            agregar_al_historial("user",mensaje)
            agregar_al_historial("assistant",odtencuin)
            chat.controls.append(crear_burbuja("Tú :", mensaje, True))
            chat.controls.append(crear_burbuja(f"Bot :",  odtencuin, False))
            
            chat.update()
        
        threading.Thread(target=procesar, daemon=True).start()
    
    def crear_burbuja(autor,texto,es_usuario):
        if es_usuario == True:
            color_fondo =  "#1a0a00"
            color_borde = "#e05c00"
            alineacion = ft.MainAxisAlignment.END
        else:
            color_fondo = "#141414"
            color_borde = "#2a2a2a"
            alineacion = ft.MainAxisAlignment.START

        burbuja = ft.Container(
            bgcolor=color_fondo,
            border=ft.border.all(1, color_borde),   
            border_radius=12,
            padding=10,
            content=ft.Column(
                controls=[
                    ft.Text(autor, color="#e05c00", size=12),
                    ft.Text(texto, color="#ffffff", size=14,no_wrap=False , width=300, enable_interactive_selection=True)
                ],
                tight=True
            ))
        fila = ft.Row(
            controls=[burbuja],
            alignment=alineacion
        )

        return fila
    
    historial= []    
    
    def agregar_al_historial(rol,mensaje):
        historial.append({"role": rol, "content": mensaje})
    
    def activar_voz():
        Texto_voz = escuchar()
        if Texto_voz:
            entrada.value = Texto_voz
            page.update()
            send_message(None)
    
    btn_enviar = ft.Button(content=ft.Text("Enviar"), on_click=send_message)
    btn_voz = ft.IconButton(
        icon=ft.Icons.MIC,
        icon_color="#b04444",
        on_click=lambda e: activar_voz()
    )
    
    page.add(
        ft.Column(controls=[
            chat,
            ft.Row(controls=[entrada, btn_enviar, btn_voz])
        ], expand=True)
    )

ft.app(target=main)