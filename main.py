import webview
import os

from backend.api import Api 

def centrar_ventana(window):
    try:
        screens = webview.screens
        if screens:
            screen = screens[0]
            x = max(0, (screen.width - window.width) // 2)
            y = max(0, (screen.height - window.height) // 2)
            window.move(x, y)
    except Exception as e:
        print(f"No se pudo centrar la ventana automáticamente: {e}")

def iniciar_app():

    api_sapiens = Api()
    from pathlib import Path

    ruta_html = Path(__file__).resolve().parent / "frontend" / "index.html"

    if not ruta_html.exists():
          raise FileNotFoundError(f"No se encontró el archivo HTML en: {ruta_html}")

    ruta_html = ruta_html.as_uri()

    ventana = webview.create_window(
     title='Sapiens - Sistema de Organización Académica',
      url=ruta_html,
      js_api=api_sapiens,
      width=1200,
     height=800,
      min_size=(800, 600),
     background_color='#f3f4f6'
    )

    api_sapiens.set_window(ventana)
    # pywebview centra la ventana automáticamente al inicio por defecto.
    # Se deshabilita el centrado manual para evitar conflictos con la escala de pantalla (DPI) en Windows 11.
    # ventana.events.shown += lambda: centrar_ventana(ventana)

    print("Iniciando Sapiens...")
    webview.start(debug=False)

if __name__ == '__main__':
    iniciar_app()
