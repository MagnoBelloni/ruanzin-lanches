#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, url_for, request, redirect, json
from flask_mysqldb import MySQL

from models.cliente import Cliente
from models.pedido import Pedido
from models.produto import Produto
from models.item import Item

from repositories.cliente import ClienteRepository
from repositories.produto import ProdutoRepository
from repositories.pedido import PedidoRepository

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "ruanzinlanches"
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)
cliente_repository = ClienteRepository(db)
produto_repository = ProdutoRepository(db)
pedido_repository = PedidoRepository(db)


@app.route("/")
def index():
    pedidos = ["X-Tudo", "X-Burguer", "Hot Dog"]

    return render_template("index.html", pedidos=pedidos)

#  ROTAS CLIENTE
@app.route("/cliente", methods=['GET', ])
def clientes():
    clientes = cliente_repository.get()

    return render_template("cliente/index.html", clientes=clientes)


@app.route("/cliente/create", methods=['GET', 'POST'])
def clientes_create():
    if request.method == 'GET':
        return render_template("cliente/create.html")
    else:
        nome = request.form['nome']
        cpf = request.form['cpf']

        cliente = Cliente(nome, cpf)
        cliente_repository.save(cliente)

        return redirect(url_for("clientes"))


@app.route("/cliente/edit/<id>", methods=['GET', 'POST'])
def clientes_update(id):
    if request.method == 'GET':
        cliente = cliente_repository.get(id)

        return render_template("cliente/edit.html", cliente=cliente, id=id)
    else:
        nome = request.form['nome']
        cpf = request.form['cpf']

        cliente = Cliente(nome, cpf, id)
        cliente_repository.save(cliente)

        return redirect(url_for("clientes"))


@app.route("/cliente/delete/<id>")
def deletar(id):
    cliente_repository.delete(id)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

#  ROTAS PRODUTO
@app.route("/produto", methods=['GET', ])
def produtos():
    produtos = produto_repository.get()

    return render_template("produto/index.html", produtos=produtos)


@app.route("/produto/create", methods=['GET', 'POST'])
def produtos_create():
    if request.method == 'GET':
        return render_template("produto/create.html")
    else:
        nome = request.form['nome']
        preco = request.form['preco']

        produto = Produto(nome, preco)
        produto_repository.save(produto)

        return redirect(url_for("produtos"))


@app.route("/produto/edit/<id>", methods=['GET', 'POST'])
def produtos_update(id):
    if request.method == 'GET':
        produtos = produto_repository.get(id)
        return render_template("produto/edit.html", produtos=produtos)
    else:
        nome = request.form['nome']
        preco = request.form['preco']

        produtos = Produto(nome, preco, id)
        produto_repository.save(produtos)

        return redirect(url_for("produtos"))


@app.route("/produto/delete/<id>")
def produtos_delete(id):
    produto_repository.delete(id)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

#  ROTAS PEDIDO
@app.route("/pedido", methods=['GET', ])
def pedidos():
    pedidos = pedido_repository.get()

    return render_template("pedido/index.html", pedidos=pedidos)


@app.route("/pedido/create", methods=['GET', 'POST'])
def pedidos_create():
    if request.method == 'GET':
        clientes = cliente_repository.get()
        produtos = produto_repository.get()

        return render_template("pedido/create.html", clientes=clientes, produtos=produtos)
    else:
        req = request.get_json()
        item = req['item']
        pedido = Pedido(req['idCliente'], item)

        pedido_repository.save(pedido)

        return jsonify({'status': 'success'})


@app.route("/pedido/edit/<id>", methods=['GET', 'POST'])
def pedidos_update(id):
    if request.method == 'GET':
        pedido = pedido_repository.get(id)
        clientes = cliente_repository.get()
        produtos = produto_repository.get()
        print(pedido)
        return render_template("pedido/edit.html", clientes=clientes, produtos=produtos, pedido=pedido)
    else:
        nome = request.form['nome']
        cpf = request.form['cpf']

        cliente = Cliente(nome, cpf, id)
        cliente_repository.save(cliente)

        return redirect(url_for("clientes"))


@app.route("/pedido/delete/<id>")
def pedido_delete(id):
    pedido_repository.delete(id)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
