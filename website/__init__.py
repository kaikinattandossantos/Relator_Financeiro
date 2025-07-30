from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DB_USER = "root"
DB_PASS = "senha123"
DB_HOST = "localhost"  
DB_NAME = "autonomo"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uma-chave-secreta-qualquer'
    
    # A linha mais importante: a nova string de conexão com o MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    
    # O resto do seu código continua exatamente igual!
    db.init_app(app)
    # ...

    # 4. Importa e registra seu Blueprint de autenticação/custos
    from .auth import auth # O nome 'auth' vem do seu arquivo auth.py
    app.register_blueprint(auth, url_prefix='/')

    # 5. Importa os modelos antes de criar o banco de dados
    from .models import Entidade # Use o nome da sua classe

    # 6. Cria o arquivo do banco de dados (se ele não existir)
    with app.app_context():
        db.create_all()

    return app