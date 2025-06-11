# Estrutura inicial do app com banco e rotas principais
# app.py
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ecommerce.db')
print("Usando banco:", db_path)

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def conectar():
    return sqlite3.connect("banco.db")

# Decoradores para controle de acesso
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('tipo') != 'adm':
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def vendedor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('tipo') != 'vendedor':
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.nome, p.descricao, p.preco, p.imagem, l.nome AS loja_nome 
        FROM produtos p 
        LEFT JOIN lojas l ON p.loja_id = l.id 
        WHERE p.status = 'ativo'
    """)
    produtos = cur.fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)


@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, 'cliente')", (nome, email, senha))
        con.commit()
        con.close()
        return redirect('/login')
    return render_template("/auth/cadastro_usuario.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id, tipo FROM usuarios WHERE email=? AND senha=?", (email, senha))
        usuario = cur.fetchone()
        con.close()

        if usuario:
            session['usuario_id'] = usuario[0]
            session['tipo'] = usuario[1]
            return redirect('/')
    return render_template("/auth/login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/cadastro_loja', methods=['GET', 'POST'])
@login_required
def cadastro_loja():
    if request.method == 'POST':
        nome = request.form['nome']
        dono_id = session['usuario_id']

        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO lojas (nome, dono_id) VALUES (?, ?)", (nome, dono_id))
        con.commit()
        con.close()
        return redirect('/')
    return render_template("cadastro_loja.html")

@app.route('/cadastro_produto', methods=['GET', 'POST'])
@login_required
def cadastro_produto():
    con = conectar()
    cur = con.cursor()

    if session['tipo'] == 'vendedor':
        cur.execute("SELECT id, nome FROM lojas WHERE dono_id=?", (session['usuario_id'],))
    elif session['tipo'] == 'adm':
        cur.execute("SELECT id, nome FROM lojas")
    else:
        return redirect('/')

    lojas = cur.fetchall()

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        imagem = request.form['imagem']
        loja_id = request.form['loja_id']
        status = 'ativo'

        cur.execute("INSERT INTO produtos (nome, descricao, preco, imagem, loja_id, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (nome, descricao, preco, imagem, loja_id, status))
        con.commit()
        con.close()
        return redirect('/')

    con.close()
    return render_template("cadastro_produto.html", lojas=lojas)

@app.route('/produtos')
def listar_produtos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT p.id, p.nome, p.descricao, p.preco, p.imagem, l.nome FROM produtos p LEFT JOIN lojas l ON p.loja_id = l.id")
    produtos = cur.fetchall()
    con.close()
    return render_template("produtos.html", produtos=produtos)

@app.route('/verificar')
def verificar():
    conn = sqlite3.connect("C:/Users/Service Desk/Documents/GitHub/ecommerce_loja_flex/ecommerce.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cur.fetchall()
    conn.close()
    return "<br>".join([t[0] for t in tabelas])


if __name__ == '__main__':
    app.run(debug=True)
