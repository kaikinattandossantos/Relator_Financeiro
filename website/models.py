from . import db



class Entidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100))
    nome = db.Column(db.String(100))
    numero = db.Column(db.String(100))
    observacao = db.Column(db.String(100))