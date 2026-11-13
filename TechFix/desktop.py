
import threading
import webview

from werkzeug.serving import make_server
from app import app, criar_tabelas


# Garante que as tabelas do banco existam
criar_tabelas()


# Inicializa o servidor Flask
servidor = make_server("127.0.0.1", 5000, app)

thread_servidor = threading.Thread(
    target=servidor.serve_forever,
    daemon=True
)


def iniciar_techfix():

    thread_servidor.start()

    # Abre a janela do aplicativo
    webview.create_window(
        title="TechFix - Assistência Técnica",
        url="http://127.0.0.1:5000",
        width=1200,
        height=800,
        min_size=(900, 600)
    )

    webview.start()


if __name__ == "__main__":

    try:
        iniciar_techfix()

    finally:
        servidor.shutdown()