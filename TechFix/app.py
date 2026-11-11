
import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, abort

# ==========================================
# INICIALIZAÇÃO DA APLICAÇÃO
# ==========================================

app = Flask(__name__)

# Caminho do banco de dados
DATABASE = os.path.join(app.root_path, "techfix.db")


# ==========================================
# CONEXÃO COM O BANCO DE DADOS
# ==========================================

def conectar_banco():
    conexao = sqlite3.connect(DATABASE)

    # Permite acessar as colunas pelo nome
    conexao.row_factory = sqlite3.Row

    return conexao


# ==========================================
# CRIAÇÃO DAS TABELAS
# ==========================================

def criar_tabelas():

    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.commit()
    conexao.close()


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

    conexao = conectar_banco()

    clientes = conexao.execute("""
        SELECT * FROM clientes
        ORDER BY id_cliente DESC
    """).fetchall()

    conexao.close()

    return render_template(
        "clientes.html",
        clientes=clientes
    )


@app.route("/clientes/cadastrar", methods=["GET", "POST"])
def cadastrar_cliente():

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not telefone:
            return render_template(
                "cadastro_cliente.html",
                erro="Preencha o nome e o telefone."
            )

        conexao = conectar_banco()

        conexao.execute("""
            INSERT INTO clientes (nome, telefone, email)
            VALUES (?, ?, ?)
        """, (nome, telefone, email))

        conexao.commit()
        conexao.close()

        return redirect(url_for("listar_clientes"))

    return render_template("cadastro_cliente.html")


# ==========================================
# EDIÇÃO DE CLIENTES
# ==========================================

@app.route("/clientes/<int:id_cliente>/editar", methods=["GET", "POST"])
def editar_cliente(id_cliente):

    conexao = conectar_banco()

    cliente = conexao.execute("""
        SELECT * FROM clientes
        WHERE id_cliente = ?
    """, (id_cliente,)).fetchone()

    if cliente is None:
        conexao.close()
        abort(404)

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not telefone:
            conexao.close()

            return render_template(
                "editar_cliente.html",
                cliente=cliente,
                erro="Preencha o nome e o telefone."
            )

        conexao.execute("""
            UPDATE clientes
            SET nome = ?, telefone = ?, email = ?
            WHERE id_cliente = ?
        """, (nome, telefone, email, id_cliente))

        conexao.commit()
        conexao.close()

        return redirect(url_for("listar_clientes"))

    conexao.close()

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )

# ==========================================
# EXCLUSÃO DE CLIENTES
# ==========================================

@app.route("/clientes/<int:id_cliente>/excluir", methods=["POST"])
def excluir_cliente(id_cliente):

    conexao = conectar_banco()

    conexao.execute("""
        DELETE FROM clientes
        WHERE id_cliente = ?
    """, (id_cliente,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("listar_clientes"))


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

    criar_tabelas()

    app.run(debug=True)