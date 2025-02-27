from src import database, login_manager
from flask_login import UserMixin
from datetime import datetime


class FuncaoUser(database.Model):
    __tablename__ = "funcao_user"
    id = database.Column(database.Integer, primary_key=True)
    ocupacao = database.Column(database.String(50), nullable=False)
    user = database.relationship('User', backref='user_funcao')


@login_manager.user_loader
def load_usuario(id_usuario):
    return TimesInscritos.query.get(int(id_usuario))


class User(database.Model):
    __tablename__ = "user"
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100))
    email = database.Column(database.String(50))
    cpf = database.Column(database.String(50), unique=True)
    senha = database.Column(database.String(500))
    funcao_user_id = database.Column(database.Integer, database.ForeignKey('funcao_user.id'))

    ip_address = database.Column(database.String(45))
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow())
    data_ultimo_acesso = database.Column(database.DateTime, default=datetime.utcnow())
    endereco_acesso = database.Column(database.String(100))

    funcao_user = database.relationship('FuncaoUser', foreign_keys=[funcao_user_id])


class TimesInscritos(database.Model, UserMixin):
    __tablename__ = "times_inscritos"
    id = database.Column(database.Integer, primary_key=True)
    nome_responsavel = database.Column(database.String(100))
    email = database.Column(database.String(50))
    telefone_responsavel = database.Column(database.String(50))
    nome_equipe = database.Column(database.String(100))
    jogador_1 = database.Column(database.String(100))
    jogador_2 = database.Column(database.String(100))
    jogador_3 = database.Column(database.String(100))
    jogador_4 = database.Column(database.String(100))
    jogador_5 = database.Column(database.String(100))
    jogador_6 = database.Column(database.String(100))
    jogador_7 = database.Column(database.String(100))
    jogador_8 = database.Column(database.String(100))
    jogador_9 = database.Column(database.String(100))
    jogador_10 = database.Column(database.String(100))

    ip_address = database.Column(database.String(45))
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow())
    data_ultimo_acesso = database.Column(database.DateTime, default=datetime.utcnow())
    endereco_acesso = database.Column(database.String(100))
    senha = database.Column(database.String(700))


class ComprovantesPagamento(database.Model):
    __tablename__ = "comprovantes_pagamento"
    id = database.Column(database.Integer, primary_key=True)
    id_time = database.Column(database.Integer, database.ForeignKey('times_inscritos.id'))
    parcela = database.Column(database.String(20))
    arquivo_comprovante = database.Column(database.String(50))
    data_envio = database.Column(database.DateTime, default=datetime.utcnow())
    status = database.Column(database.String(50))
