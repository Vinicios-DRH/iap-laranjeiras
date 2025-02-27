from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField)
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email, Optional
from src.models import TimesInscritos


class FormCriarUsuario(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[Optional(), Length(6, 20)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
                                    Optional(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Salvar')

    def validate_email(self, email):
        # Obtenha o usuário do formulário, se disponível
        current_user_id = getattr(self, 'current_user_id', None)
        if current_user_id:
            usuario = TimesInscritos.query.filter(
                TimesInscritos.email == email.data, TimesInscritos.id != current_user_id).first()
        else:
            usuario = TimesInscritos.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError(
                'E-mail já cadastrado. Cadastre-se com outro e-mail ou faça Login para continuar.')


class FormInscricaoTorneio(FlaskForm):
    nome_responsavel = StringField(
        'Nome Completo do responsável', validators=[DataRequired()])
    email = StringField('E-mail do responsável',
                        validators=[DataRequired(), Email()])
    telefone_responsavel = StringField(
        'Telefone do responsável', validators=[DataRequired()])
    nome_equipe = StringField('Nome da equipe', validators=[DataRequired()])
    jogador_1 = StringField('Jogador 1', validators=[DataRequired()])
    jogador_2 = StringField('Jogador 2', validators=[DataRequired()])
    jogador_3 = StringField('Jogador 3', validators=[DataRequired()])
    jogador_4 = StringField('Jogador 4', validators=[DataRequired()])
    jogador_5 = StringField('Jogador 5', validators=[DataRequired()])
    jogador_6 = StringField('Jogador 6', validators=[DataRequired()])
    jogador_7 = StringField('Jogador 7', validators=[DataRequired()])
    jogador_8 = StringField('Jogador 8', validators=[DataRequired()])
    jogador_9 = StringField('Jogador 9', validators=[DataRequired()])
    jogador_10 = StringField('Jogador 10', validators=[DataRequired()])
    aviso_informacoes = BooleanField(
        'Desejo receber notificações no meu e-mail cadastrado.')
    lembrar_ciente = BooleanField(
        'Estou ciente de pagar a primeira parcela sem direito a devolução')
    botao_submit_inscrever = SubmitField('Enviar')

    def validate_email(self, email):
        # Obtenha o usuário do formulário, se disponível
        current_user_id = getattr(self, 'current_user_id', None)
        if current_user_id:
            usuario = TimesInscritos.query.filter(
                TimesInscritos.email == email.data, TimesInscritos.id != current_user_id).first()
        else:
            usuario = TimesInscritos.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError('E-mail já cadastrado.')


class FormLoginTime(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Mantenha-me logado')
    botao_submit_login = SubmitField('Entrar')
