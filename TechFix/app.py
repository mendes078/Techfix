
from flask import Flask, render_template

# Inicialização da aplicação
app = Flask(__name__)


# ==========================================
# ROTAS PRINCIPAIS
# ==========================================

@app.route("/")
def inicio():
    return render_template("dashboard.html")


# ==========================================
# ROTAS DE CLIENTES
# ==========================================

@app.route("/clientes")
def listar_clientes():
    return render_template("clientes.html")


@app.route("/clientes/cadastrar")
def cadastrar_cliente():
    return render_template("cadastro_cliente.html")


@app.route("/clientes/<int:id_cliente>")
def detalhes_cliente(id_cliente):
    return f"Detalhes do cliente {id_cliente}"


# ==========================================
# ROTAS DE APARELHOS
# ==========================================

@app.route("/aparelhos")
def listar_aparelhos():
    return render_template("aparelhos.html")


@app.route("/aparelhos/cadastrar")
def cadastrar_aparelho():
    return render_template("cadastro_aparelho.html")


# ==========================================
# EXECUÇÃO DA APLICAÇÃO
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)