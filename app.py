# app.py
from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
import os
from banco import (
    criar_usuario, autenticar_usuario, criar_loja, listar_lojas,
    criar_produto, listar_produtos
)

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

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
    produtos = listar_produtos(ativos=True)
    return render_template('index.html', produtos=produtos)

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        criar_usuario(nome, email, senha)
        return redirect('/login')
    return render_template("/auth/cadastro_usuario.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = autenticar_usuario(email, senha)
        if usuario:
            session['usuario_id'] = usuario.id
            session['tipo'] = usuario.tipo
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
        criar_loja(nome=nome, dono_id=dono_id)
        return redirect('/')
    return render_template("cadastro_loja.html")

@app.route('/cadastro_produto', methods=['GET', 'POST'])
@login_required
def cadastro_produto():
    tipo = session['tipo']
    usuario_id = session['usuario_id']
    lojas = listar_lojas(usuario_id if tipo == 'vendedor' else None)

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        imagem = request.form['imagem']
        loja_id = int(request.form['loja_id'])
        criar_produto(nome, descricao, preco, loja_id, imagem)
        return redirect('/')

    return render_template("cadastro_produto.html", lojas=lojas)

@app.route('/produtos')
def listar_produtos_view():
    produtos = listar_produtos(ativos=False)
    return render_template("produtos.html", produtos=produtos)

@app.route('/verificar')
def verificar():
    from banco import Base, engine
    insp = engine.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    return "<br>".join([t[0] for t in insp])

if __name__ == '__main__':
    app.run(debug=True)