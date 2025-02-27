from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import login_required, current_user, login_user
from src import app, bcrypt, database
from src.models import TimesInscritos, ComprovantesPagamento
from src.forms import FormInscricaoTorneio, FormLoginTime
from datetime import datetime
import os
from werkzeug.utils import secure_filename


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('candidato'))
    return redirect(url_for('info'))


@app.route("/info", methods=['GET', 'POST'])
def info():
    return render_template('info.html')


def get_user_ip():
    # Verifica se o cabeçalho X-Forwarded-For está presente
    if request.headers.get('X-Forwarded-For'):
        # Pode conter múltiplos IPs, estou pegando o primeiro
        ip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        # Fallback para o IP remoto
        ip = request.remote_addr
    return ip


@app.route("/login", methods=['GET', 'POST'])
def login():
    flash('Sua senha é seu número de telefone', 'alert-info')
    if current_user.is_authenticated:
        flash('Você já está logado.', 'alert-info')
        return redirect(url_for('candidato'))

    form_login = FormLoginTime()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        user = TimesInscritos.query.filter_by(email=form_login.email.data).first()

        if user and bcrypt.check_password_hash(user.senha, form_login.senha.data):
            login_user(user, remember=form_login.lembrar_dados.data)
            flash('Login feito com sucesso!', 'alert-success')
            return redirect(url_for('candidato'))

        else:
            flash('Falha no Login, e-mail ou senha incorretos.', 'alert-danger')

    return render_template('login_time.html', form_login=form_login)


@app.route("/inscricao", methods=['GET', 'POST'])
def inscricao():
    if current_user.is_authenticated:
        return redirect(url_for('candidato'))
    form_inscricao = FormInscricaoTorneio()

    if form_inscricao.validate_on_submit():
        print("Formulário validado e enviado!")
        senha_cript = bcrypt.generate_password_hash(form_inscricao.telefone_responsavel.data).decode('utf-8')
        print(f"Senha gerada: {senha_cript}")
        time_inscrito = TimesInscritos(nome_responsavel=form_inscricao.nome_responsavel.data,
                                       email=form_inscricao.email.data,
                                       telefone_responsavel=form_inscricao.telefone_responsavel.data,
                                       nome_equipe=form_inscricao.nome_equipe.data,
                                       jogador_1=form_inscricao.jogador_1.data,
                                       jogador_2=form_inscricao.jogador_2.data,
                                       jogador_3=form_inscricao.jogador_3.data,
                                       jogador_4=form_inscricao.jogador_4.data,
                                       jogador_5=form_inscricao.jogador_5.data,
                                       jogador_6=form_inscricao.jogador_6.data,
                                       jogador_7=form_inscricao.jogador_7.data,
                                       jogador_8=form_inscricao.jogador_8.data,
                                       jogador_9=form_inscricao.jogador_9.data,
                                       jogador_10=form_inscricao.jogador_10.data,
                                       ip_address=get_user_ip(),
                                       data_criacao=datetime.now(),
                                       senha=senha_cript)

        database.session.add(time_inscrito)
        database.session.commit()
        return redirect(url_for('candidato'))
    else:
        print(form_inscricao.errors)
    return render_template('inscricao.html', form_inscricao=form_inscricao)


@app.route("/candidato", methods=['GET', 'POST'])
@login_required
def candidato():
    form_inscricao = FormInscricaoTorneio()

    time = TimesInscritos.query.filter_by(id=current_user.id).first()

    if time:
        form_inscricao.nome_equipe.data = time.nome_equipe
        form_inscricao.jogador_1.data = time.jogador_1
        form_inscricao.jogador_2.data = time.jogador_2
        form_inscricao.jogador_3.data = time.jogador_3
        form_inscricao.jogador_4.data = time.jogador_4
        form_inscricao.jogador_5.data = time.jogador_5
        form_inscricao.jogador_6.data = time.jogador_6
        form_inscricao.jogador_7.data = time.jogador_7
        form_inscricao.jogador_8.data = time.jogador_8
        form_inscricao.jogador_9.data = time.jogador_9
        form_inscricao.jogador_10.data = time.jogador_10

    return render_template('candidato.html', form_inscricao=form_inscricao)


ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}  # Defina as extensões permitidas


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload_comprovante", methods=['POST'])
@login_required
def upload_comprovante():
    if 'arquivo' not in request.files:
        return jsonify({"status": "erro", "mensagem": "Nenhum arquivo enviado"}), 400

    file = request.files['arquivo']
    parcela = request.form.get('parcela', '')

    if file.filename == '':
        return jsonify({"status": "erro", "mensagem": "Nenhum arquivo selecionado"}), 400

    if file and allowed_file(file.filename):
        # Segurança: Garante um nome seguro para o arquivo
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Obtém o time do usuário atual
        time = TimesInscritos.query.filter_by(id=current_user.id).first()
        if not time:
            return jsonify({"status": "erro", "mensagem": "Time não encontrado"}), 400

        # Criando o registro no banco de dados
        comprovante = ComprovantesPagamento(
            id_time=time.id,
            parcela=parcela,
            arquivo_comprovante=filename,
            data_envio=datetime.utcnow(),
            status="Pendente"
        )

        database.session.add(comprovante)
        database.session.commit()

        return jsonify({"status": "sucesso", "mensagem": "Comprovante enviado com sucesso!"}), 200

    return jsonify({"status": "erro", "mensagem": "Arquivo não permitido"}), 400


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
