from flask import render_template, redirect, request, session, flash, url_for
from models import *
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
    if 'User_Only' not in session or session['User_Only'] == None:
        return redirect('login') 
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
@app.route('/editar')
def edit():
    return render_template('edit.html')

    
@app.route('/editar_produto/<int:produto_id>', methods=['GET'])
def editar_produto(produto_id):
    if 'User_Only' not in session or session['User_Only'] == None:
        return redirect('login') 
    # Buscar o produto pelo ID
    produto = Produtos.query.get(produto_id)
    if produto:
        # Renderizar o template de edição com os detalhes do produto
        return render_template('edit.html', produto=produto)
    else:
        flash("Produto não encontrado.")
        return redirect('/')

@app.route('/salvar_edicao/<int:produto_id>', methods=['POST'])
def salvar_edicao(produto_id):
    # Buscar o produto pelo ID
    produto = Produtos.query.get(produto_id)

    if produto:
        # Atualizar os atributos do produto com base nos dados do formulário
        produto.rastreio_pedido = request.form['txtRastreio']
        produto.tipo_prod = request.form['txtTipo']
        produto.datareceb_prod = request.form['txtData']
        produto.desc_prod = request.form['txtDescricao']

        # Commit para salvar as mudanças no banco de dados
        db.session.commit()

        flash("Produto editado com sucesso.")
    else:
        flash("Produto não encontrado.")

    return redirect('/')

@app.route('/pesquisar_rastreio', methods=['POST'])
def pesquisar_rastreio():
    # Verifica se foi enviado um parâmetro de busca
    rastreio = request.form['rastreio']

    if rastreio:
        # Realiza a busca no banco de dados pelo número de rastreamento
        produto = Produtos.query.filter(Produtos.rastreio_pedido.ilike(f'%{rastreio}%')).first()
        if produto:
            # Se o produto for encontrado, redireciona para a página de edição
            return redirect(url_for('editar_produto', produto_id=produto.id_produto))
        else:
            flash('Produto não encontrado com o número de rastreamento informado.')
            return redirect(url_for('paginaInicial'))
    else:
        flash('Informe o número de rastreamento para realizar a pesquisa.')
        return redirect(url_for('paginaInicial'))

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

@app.route('/logout', methods=['POST'])
def logout():
    # Remova o usuário da sessão
    session.pop('User_Only', None)
    # Redirecione para a página de login
    return redirect(url_for('login'))

app.run(debug=True)


