from flask import render_template, redirect, request, session, flash, url_for
from models import Produtos, Usuarios
from main import db, app

# Rotas 
@app.route("/")
def paginaInicial():
    if 'User_Only' not in session or session['User_Only'] == None:
        return redirect('login') 
    produtos_cadastrados = Produtos.query.order_by(Produtos.id_produto).all()
    return render_template("index.html", Produtos = produtos_cadastrados  )

@app.route('/cadastrar')
def cadastrar_produto():
    return render_template('cadastrar_produto.html')

@app.route('/login')
def login():
   return render_template('Login.html')
    
@app.route('/logar', methods=['POST'])
def logar():
    usuario =  Usuarios.query.filter_by(mail = request.form['txtEmail']).first()
    if usuario:
        if  request.form['txtSenha'] == usuario.passW:
            session['User_Only'] = usuario.name_user
            flash("Usuario Logado")
            return redirect(url_for('paginaInicial'))
        else:
            flash('senha Incorreta!')
            return redirect(url_for('login'))
    else:
        flash("Usuario/Senha Incorreta!")
        return render_template('Login.html')
    
@app.route('/registro')
def registro ():
    return render_template('reg.html')


@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    rastreio = request.form['txtRastreio']
    tipo = request.form['txtTipo']
    data = request.form['txtData']
    descricao = request.form['txtDescricao']

    produto_adicionado = Produtos(
        rastreio_pedido=rastreio,
        datareceb_prod=data,
        tipo_prod=tipo,
        desc_prod=descricao
    )

    db.session.add(produto_adicionado)
    db.session.commit()

    return redirect('/')
@app.route('/apagar_produto/<int:produto_id>', methods=['GET'])
def apagar_produto(produto_id):
    produto = Produtos.query.get(produto_id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
        flash("Produto apagado com sucesso.")
    else:
        flash("Produto não encontrado.")
    return redirect('/')
app.run(debug=True)