
import os
import sqlite3
import sys

from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime

# ==========================================
# INICIALIZAÇÃO DA APLICAÇÃO
# ==========================================

app = Flask(__name__)

# Caminho do banco de dados
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = app.root_path

DATABASE = os.path.join(BASE_DIR, "techfix.db")


# ==========================================
# CONEXÃO COM O BANCO DE DADOS
# ==========================================

def conectar_banco():
    conexao = sqlite3.connect(DATABASE)

    # Permite acessar as colunas pelo nome
    conexao.row_factory = sqlite3.Row

    # Habilita a integridade referencial
    conexao.execute("PRAGMA foreign_keys = ON")

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

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS aparelhos (
            id_aparelho INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            numero_serie TEXT,
            descricao TEXT,

            FOREIGN KEY (id_cliente)
                REFERENCES clientes(id_cliente)
        )
    """)


    conexao.execute("""
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id_os INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aparelho INTEGER NOT NULL,
            defeito_relatado TEXT NOT NULL,
            diagnostico TEXT,
            status TEXT NOT NULL DEFAULT 'Aguardando avaliação',
            valor_servico REAL NOT NULL DEFAULT 0,
            data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_conclusao TIMESTAMP,
            observacoes TEXT,

            FOREIGN KEY (id_aparelho)
                REFERENCES aparelhos(id_aparelho)
        )
    """)

    conexao.commit()
    conexao.close()


# ==========================================
# ROTAS PRINCIPAIS
# ==========================================

@app.route("/")
def inicio():

    conexao = conectar_banco()

    # Total de clientes cadastrados
    total_clientes = conexao.execute("""
        SELECT COUNT(*)
        FROM clientes
    """).fetchone()[0]

    # Total de aparelhos cadastrados
    total_aparelhos = conexao.execute("""
        SELECT COUNT(*)
        FROM aparelhos
    """).fetchone()[0]

    # Total de ordens de serviço
    total_ordens = conexao.execute("""
        SELECT COUNT(*)
        FROM ordens_servico
    """).fetchone()[0]

    # Faturamento dos serviços concluídos ou entregues
    faturamento = conexao.execute("""
        SELECT COALESCE(SUM(valor_servico), 0)
        FROM ordens_servico
        WHERE status IN ('Concluído', 'Entregue')
    """).fetchone()[0]

    conexao.close()

    # Formatação monetária brasileira
    faturamento_formatado = (
        f"R$ {faturamento:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return render_template(
        "dashboard.html",
        total_clientes=total_clientes,
        total_aparelhos=total_aparelhos,
        total_ordens=total_ordens,
        faturamento=faturamento_formatado
    )

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

    conexao = conectar_banco()

    aparelhos = conexao.execute("""
        SELECT
            aparelhos.id_aparelho,
            aparelhos.id_cliente,
            aparelhos.tipo,
            aparelhos.marca,
            aparelhos.modelo,
            aparelhos.numero_serie,
            clientes.nome AS nome_cliente

        FROM aparelhos

        INNER JOIN clientes
            ON aparelhos.id_cliente = clientes.id_cliente

        ORDER BY aparelhos.id_aparelho DESC
    """).fetchall()

    conexao.close()

    return render_template(
        "aparelhos.html",
        aparelhos=aparelhos
    )

@app.route("/aparelhos/cadastrar", methods=["GET", "POST"])
def cadastrar_aparelho():

    conexao = conectar_banco()

    # Busca os clientes para preencher o campo de seleção
    clientes = conexao.execute("""
        SELECT id_cliente, nome
        FROM clientes
        ORDER BY nome ASC
    """).fetchall()

    if request.method == "POST":

        id_cliente = request.form.get("id_cliente", type=int)
        tipo = request.form.get("tipo", "").strip()
        marca = request.form.get("marca", "").strip()
        modelo = request.form.get("modelo", "").strip()
        numero_serie = request.form.get("numero_serie", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not id_cliente or not tipo or not marca or not modelo:
            conexao.close()

            return render_template(
                "cadastro_aparelho.html",
                clientes=clientes,
                erro="Preencha todos os campos obrigatórios."
            )

        conexao.execute("""
            INSERT INTO aparelhos (
                id_cliente,
                tipo,
                marca,
                modelo,
                numero_serie,
                descricao
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            id_cliente,
            tipo,
            marca,
            modelo,
            numero_serie,
            descricao
        ))

        conexao.commit()
        conexao.close()

        return redirect(url_for("listar_aparelhos"))

    conexao.close()

    return render_template(
        "cadastro_aparelho.html",
        clientes=clientes
    )


@app.route("/aparelhos/<int:id_aparelho>/editar", methods=["GET", "POST"])
def editar_aparelho(id_aparelho):

    conexao = conectar_banco()

    aparelho = conexao.execute("""
        SELECT *
        FROM aparelhos
        WHERE id_aparelho = ?
    """, (id_aparelho,)).fetchone()

    if aparelho is None:
        conexao.close()
        abort(404)

    clientes = conexao.execute("""
        SELECT id_cliente, nome
        FROM clientes
        ORDER BY nome ASC
    """).fetchall()

    if request.method == "POST":

        id_cliente = request.form.get("id_cliente", type=int)
        tipo = request.form.get("tipo", "").strip()
        marca = request.form.get("marca", "").strip()
        modelo = request.form.get("modelo", "").strip()
        numero_serie = request.form.get("numero_serie", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not id_cliente or not tipo or not marca or not modelo:
            conexao.close()
            return render_template(
                "editar_aparelho.html",
                aparelho=aparelho,
                clientes=clientes,
                erro="Preencha todos os campos obrigatórios."
            )

        conexao.execute("""
            UPDATE aparelhos
            SET
                id_cliente = ?,
                tipo = ?,
                marca = ?,
                modelo = ?,
                numero_serie = ?,
                descricao = ?
            WHERE id_aparelho = ?
        """, (
            id_cliente,
            tipo,
            marca,
            modelo,
            numero_serie,
            descricao,
            id_aparelho
        ))

        conexao.commit()
        conexao.close()

        return redirect(url_for("listar_aparelhos"))

    conexao.close()

    return render_template(
        "editar_aparelho.html",
        aparelho=aparelho,
        clientes=clientes
    )


@app.route("/aparelhos/<int:id_aparelho>/excluir", methods=["POST"])
def excluir_aparelho(id_aparelho):

    conexao = conectar_banco()

    conexao.execute("""
        DELETE FROM aparelhos
        WHERE id_aparelho = ?
    """, (id_aparelho,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("listar_aparelhos"))


@app.route("/ordens-servico/cadastrar", methods=["GET", "POST"])
def cadastrar_ordem_servico():

    conexao = conectar_banco()

    aparelhos = conexao.execute("""
        SELECT
            aparelhos.id_aparelho,
            aparelhos.tipo,
            aparelhos.marca,
            aparelhos.modelo,
            clientes.nome AS nome_cliente
        FROM aparelhos
        INNER JOIN clientes
            ON aparelhos.id_cliente = clientes.id_cliente
        ORDER BY aparelhos.id_aparelho DESC
    """).fetchall()

    if request.method == "POST":

        id_aparelho = request.form.get("id_aparelho", type=int)
        defeito_relatado = request.form.get(
            "defeito_relatado", ""
        ).strip()
        observacoes = request.form.get("observacoes", "").strip()

        if not id_aparelho or not defeito_relatado:
            conexao.close()

            return render_template(
                "cadastro_ordem_servico.html",
                aparelhos=aparelhos,
                erro="Selecione um aparelho e informe o defeito relatado."
            )

        conexao.execute("""
            INSERT INTO ordens_servico (
                id_aparelho,
                defeito_relatado,
                observacoes
            )
            VALUES (?, ?, ?)
        """, (
            id_aparelho,
            defeito_relatado,
            observacoes
        ))

        conexao.commit()
        conexao.close()

        return redirect(
            url_for("cadastrar_ordem_servico", sucesso=1)
        )

    conexao.close()

    return render_template(
        "cadastro_ordem_servico.html",
        aparelhos=aparelhos
    )


@app.route("/ordens-servico")
def listar_ordens_servico():

    conexao = conectar_banco()

    ordens = conexao.execute("""
        SELECT
            ordens_servico.id_os,
            ordens_servico.defeito_relatado,
            ordens_servico.status,
            ordens_servico.valor_servico,
            ordens_servico.data_abertura,
            ordens_servico.data_conclusao,
            aparelhos.tipo,
            aparelhos.marca,
            aparelhos.modelo,
            clientes.nome AS nome_cliente
        FROM ordens_servico
        INNER JOIN aparelhos
            ON ordens_servico.id_aparelho = aparelhos.id_aparelho
        INNER JOIN clientes
            ON aparelhos.id_cliente = clientes.id_cliente
        ORDER BY ordens_servico.id_os DESC
    """).fetchall()

    conexao.close()

    return render_template(
        "ordens_servico.html",
        ordens=ordens
    )



@app.route("/ordens-servico/<int:id_os>/editar", methods=["GET", "POST"])
def editar_ordem_servico(id_os):

    conexao = conectar_banco()

    ordem = conexao.execute("""
        SELECT
            ordens_servico.*,
            aparelhos.tipo,
            aparelhos.marca,
            aparelhos.modelo,
            clientes.nome AS nome_cliente
        FROM ordens_servico
        INNER JOIN aparelhos
            ON ordens_servico.id_aparelho = aparelhos.id_aparelho
        INNER JOIN clientes
            ON aparelhos.id_cliente = clientes.id_cliente
        WHERE ordens_servico.id_os = ?
    """, (id_os,)).fetchone()

    if ordem is None:
        conexao.close()
        abort(404)

    if request.method == "POST":

        diagnostico = request.form.get(
            "diagnostico", ""
        ).strip()

        status = request.form.get(
            "status", ""
        ).strip()

        valor_servico = request.form.get(
            "valor_servico", type=float
        )

        data_conclusao = request.form.get(
            "data_conclusao"
        ) or None

        observacoes = request.form.get(
            "observacoes", ""
        ).strip()

        status_validos = [
            "Aguardando avaliação",
            "Em diagnóstico",
            "Aguardando aprovação",
            "Aguardando peças",
            "Em conserto",
            "Concluído",
            "Entregue",
            "Cancelado"
        ]

        if status not in status_validos:
            conexao.close()
            abort(400)

        if valor_servico is None or valor_servico < 0:
            conexao.close()

            return render_template(
                "editar_ordem_servico.html",
                ordem=ordem,
                erro="Informe um valor válido para o serviço."
            )

        # Preenche a data automaticamente quando o serviço
        # é concluído ou entregue.
        if status in ["Concluído", "Entregue"] and not data_conclusao:

            data_conclusao = datetime.now().strftime("%Y-%m-%d")

        conexao.execute("""
            UPDATE ordens_servico
            SET
                diagnostico = ?,
                status = ?,
                valor_servico = ?,
                data_conclusao = ?,
                observacoes = ?
            WHERE id_os = ?
        """, (
            diagnostico,
            status,
            valor_servico,
            data_conclusao,
            observacoes,
            id_os
        ))

        conexao.commit()
        conexao.close()

        return redirect(url_for("listar_ordens_servico"))

    conexao.close()

    return render_template(
        "editar_ordem_servico.html",
        ordem=ordem
    )

@app.route("/ordens-servico/<int:id_os>")
def detalhes_ordem_servico(id_os):

    conexao = conectar_banco()

    ordem = conexao.execute("""
        SELECT
            ordens_servico.*,
            aparelhos.tipo,
            aparelhos.marca,
            aparelhos.modelo,
            aparelhos.numero_serie,
            aparelhos.descricao AS descricao_aparelho,
            clientes.id_cliente,
            clientes.nome AS nome_cliente,
            clientes.telefone,
            clientes.email
        FROM ordens_servico

        INNER JOIN aparelhos
            ON ordens_servico.id_aparelho = aparelhos.id_aparelho

        INNER JOIN clientes
            ON aparelhos.id_cliente = clientes.id_cliente

        WHERE ordens_servico.id_os = ?
    """, (id_os,)).fetchone()

    conexao.close()

    if ordem is None:
        abort(404)

    return render_template(
        "detalhes_ordem_servico.html",
        ordem=ordem
    )

# ==========================================
# EXECUÇÃO DA APLICAÇÃO
# ==========================================

if __name__ == "__main__":

    criar_tabelas()

    app.run(debug=True)