from flask import Flask, render_template, request, redirect

app = Flask(__name__)

carrinho = [
    {"id": 1, "nome": "Camisa Anime", "descricao": "100% algodão", "preco": 39.90, "imagem": "https://a.storyblok.com/f/178900/1920x1080/d2ef1671e2/bluelock.jpg/m/1200x0/filters:quality(95)format(webp)"},
    {"id": 3, "nome": "Camisa Anime", "descricao": "100% algodão", "preco": 39.90, "imagem": "https://jornalismorio.espm.br/wp-content/uploads/2021/12/confira-agora-os-25-melhores-animes-que-ja-foram-criados-1.jpg"},
    {"id": 4, "nome": "Camisa Anime", "descricao": "100% algodão", "preco": 39.90, "imagem": "https://animeflix.com.br/wp-content/uploads/2025/05/Animes-populares.jpg"},
    {"id": 2, "nome": "Mochila Naruto", "descricao": "Ideal para escola", "preco": 79.90, "imagem": "/static/img/mochila.jpg"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastroP')
def cadastroP():
    return render_template("cadastro.html")

@app.route("/pagamentos")
def pagamentos():
    return render_template("pagamento.html")

@app.route("/carrinho")
def ver_carrinho():
    return render_template("carrinho.html", carrinho=carrinho)

@app.route("/remover/<int:item_id>", methods=["POST"])
def remover_item(item_id):
    global carrinho
    carrinho = [item for item in carrinho if item["id"] != item_id]
    return redirect("/carrinho")

@app.route("/comprar/<int:item_id>", methods=["POST"])
def comprar_item():
    # Simulação de compra
    return render_template("pagamento.html")

if __name__ == '__main__':
    app.run(debug=True)
