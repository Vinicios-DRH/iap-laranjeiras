from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sistema'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iap-sistema.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.ganrmjfgmquqetvutmkg:iapLaranjeiras@aws-0-us-west-1.pooler.supabase.com:6543/postgres'

app.config['SECRET_KEY'] = '60cc737479829f9462369024bee383ce'
app.jinja_env.globals.update(enumerate=enumerate)

# Configuração do diretório de uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")  # Pasta de uploads no servidor

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'jpg', 'jpeg', 'png'}


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from src import routes