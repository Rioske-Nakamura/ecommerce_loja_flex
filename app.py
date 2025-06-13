# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from banco import *

app = Flask(__name__)
app.secret_key = 'segredo123'

@app.route('/')
def index():
    produtos = listar_produtos()
    lojas = listar_lojas() 
    return render_template('index.html', produtos=produtos, lojas=lojas)

from flask import Flask, render_template, request, redirect, url_for, session, flash
from banco import autenticar_usuario, Usuario, Session

@app.route("/login", methods=["GET", "POST"])
def login():
    mensagem = ""
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = autenticar_usuario(email, senha)

        if usuario:
            session["usuario"] = usuario.to_dict()

            return redirect(url_for("index"))  # redireciona após login
        else:
            mensagem = "❌ Email ou senha incorretos."

    return render_template("/auth/login.html", mensagem=mensagem)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    mensagem = ""
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        tipo = request.form["tipo"]

        session = Session()
        usuario_existente = session.query(Usuario).filter_by(email=email).first()

        if usuario_existente:
            mensagem = "⚠️ Este email já está cadastrado. Tente outro."
        else:
            novo = Usuario(nome=nome, email=email, senha=senha, tipo=tipo)
            session.add(novo)
            session.commit()
            session.close()
            return redirect(url_for("login"))  # ou para onde desejar após cadastro

        session.close()

    return render_template("/auth/cadastro_usuario.html", mensagem=mensagem)


@app.route('/produto/<int:produto_id>/carrinho')
def adicionar_carrinho(produto_id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    usuario_id = session['usuario']['id']
    adicionar_ao_carrinho(usuario_id, produto_id)
    return redirect(url_for('carrinho'))

@app.route('/carrinho')
def carrinho():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    itens = listar_carrinho(session['usuario']['id'])
    return render_template('carrinho.html', itens=itens)

@app.route('/finalizar')
def finalizar():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    finalizar_compra(session['usuario']['id'])
    return redirect(url_for('index'))

@app.route('/pedidos')
def pedidos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    session_db = Session()
    pedidos = session_db.query(Pedido).filter_by(cliente_id=session['usuario']['id']).all()
    session_db.close()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/pedido/<int:pedido_id>/status', methods=['POST'])
def atualizar_status(pedido_id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    novo_status = request.form['status']
    usuario = Session().query(Usuario).get(session['usuario']['id'])
    alterar_status_pedido(pedido_id, usuario, novo_status)
    return redirect(url_for('pedidos'))

@app.route('/minhas_lojas')
def minhas_lojas():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    lojas = listar_lojas(session['usuario']['id'])
    return render_template('/sale/minhas_lojas.html', lojas=lojas)

@app.route('/loja/nova', methods=['GET', 'POST'])
def nova_loja():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        

        criar_loja(
            nome=request.form['nome'],
            dono_id=session['usuario']['id'],
            CNPJ=request.form.get('cnpj'),
            descricao=request.form.get('descricao'),
            ramo=request.form.get('ramo')
        )
        return redirect(url_for('minhas_lojas'))
    return render_template('/sale/cadastro_loja.html')

@app.route('/loja/<int:loja_id>/produtos')
def produtos_loja(loja_id):
    session_db = Session()
    produtos = session_db.query(Produto).filter_by(loja_id=loja_id).all()
    session_db.close()
    return render_template('produtos_loja.html', produtos=produtos, loja_id=loja_id)

@app.route('/produto/novo/<int:loja_id>', methods=['GET', 'POST'])
def novo_produto(loja_id):
    if request.method == 'POST':
        criar_produto(
            nome=request.form['nome'],
            descricao=request.form['descricao'],
            preco=float(request.form['preco']),
            loja_id=loja_id
        )
        return redirect(url_for('produtos_loja', loja_id=loja_id))
    return render_template('/sale/cadastro_produto.html', loja_id=loja_id)

if __name__ == '__main__':
    app.run(debug=True)
