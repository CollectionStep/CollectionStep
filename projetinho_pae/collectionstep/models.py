from main import db


class Produtos(db.Model):
    __tablename__ = 'produtos'
    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rastreio_pedido = db.Column(db.String(50), nullable=False)
    datareceb_prod = db.Column(db.String(20), nullable=False)
    tipo_prod = db.Column(db.String(50), nullable=False)
    desc_prod = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Produto %r>' % self.rastreio_pedido
    
class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_user = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(50), nullable=False)
    passW = db.Column(db.String(20), nullable=False)
    def __repr__(self):
            return '<name %r>' %self.name
