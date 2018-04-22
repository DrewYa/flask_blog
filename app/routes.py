from flask import g
from flask import make_response, request
from flask import redirect, abort
from flask import render_template
from flask import url_for, session, flash

# первый app - Это название пакета, а второй - экземпляр класса Flask из модуля __init__.py
from app import app
# ---------------------
from flask_bootstrap import Bootstrap 

from datetime import datetime
from flask_moment import Moment # JS для работы со временем

from werkzeug.utils import secure_filename #

# from flask_debugtoolbar import DebugToolbarExtension

import os

# ---------------------

from app._wtForms import MyForm, LoginForm, LogoutForm, SigninForm
# можно просто писать from ._wtForms import MyForm
# т.е. без указания названия пакета
from ._wtForms import PhotoForm
# -------------------
# app = Flask(__name__) # (?)
bootstrap = Bootstrap(app)
moment = Moment(app)

# --------------------------------
# полезненькое расширение
# toolbar = DebugToolbarExtension(app)

# --------------------------------
fix_time = datetime.utcnow()
# session['_flashes'] += ['hi', 'hi Guest!']


# import _models_bd as models

# ------------
from time import sleep
# --------------------------------

@app.route('/')
def index():
	url_mp = str(app.url_map).replace('<R', '<p>R')
	url_mp = url_mp.replace('->', ' ---- name of function: ')
	url_mp = url_mp.replace('>,', '</p><br>')
	return '<h1>full list site url:</h1>\n<p>%s</p>' % url_mp
	# return (<htmlШаблон>, <кодОтвета>, <словарьЗаголовков>)
	# или return <объект Response>

@app.route('/lst_map') 
def map():
	return render_template('list_map.html', lst_map=app.url_map)

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
		'favicon.ico', mimetype='image/vnd.microsoft.icon')
 
 # ------------------------------------

@app.route('/user/')
@app.route('/user/<name>')
def user(name=None):
	if name == None:
		if session.get('username'):
			return 'in session'	+ session.get('username')		
		else:
			return redirect(url_for('login'))
	if name != session.get('username'):
		# return redirect(url_for('login'))
		abort(404)
	return render_template('user.html', name=name)

@app.route('/aboutme')
def about_me():
	flash('можешь оставить свое сообщение в форме, когда я ее сделаю :)')
	return render_template('aboutMe.html', 
		current_time=fix_time)	# datetime.utcnow())

@app.route('/present/<name>')
def present(name):
	return render_template('base.html')

@app.route('/user_agent')
def usr_agent():
	user_agent = request.headers.get('User-Agent')
	return '<p>your brower is %s</p>' % user_agent

@app.route('/make_response')
def mr():
	response = make_response('<h1>f. make_response</h1>')
	# response = make_response('<h1>hi</h1>', 200, )
	# set_cookie принимает 1 или 2 значения только
	response.set_cookie('a', '712') 
	return response

# ф. redirect перенаправляет на указанный url (отностильный или абсолют)
@app.route('/redirect')
def redir():
	return redirect('http://flask.pocoo.org')

# вместо этой ф. можно сделать так:
@app.route('/redirect2')
def redir2():
	response = make_response('', 302)
	response.headers['Location'] = 'http://flask.pocoo.org'
	return response

# ф. abort исп для обработки ошибок
# ф. не передает управление вызвавшей ее ф., а передает его веб-серверу, возбуждая исключение
@app.route('/abort/<id>') 
def abrt(id):
	if id == '2':
		abort(404) # страница не найдена
	if id == '3':
		abort(500) # внутренняя серверная ошибка
	if id == '4':
		abort(403) # нет доступа
	return '<h1>ты ввел %s, попробуй ввести abort/2 и 3 и больше </h1>' % id

# как и ф. представления, обработчики ошибок возвращают ответ с 
# числовым кодом состояния
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@app.errorhandler(403)
def not_permission(e):
	return render_template('403.html'), 403

from app import db
from app._models_bd import User, Post

@app.route('/login', methods=('GET', 'POST'))
def login():
	form = LoginForm()
	if form.validate_on_submit():
		usr = User.query.filter( (User.username==form.username.data) & 
				(User.password_hash==form.password.data) )[:1]
		if usr:
			session['username'] = form.username.data
			session['pas'] = form.password.data
			# session['usr'] = usr 		объекты сериализуются в JSON, но этот объект невозможно сериализовать (ошибка)
			flash('был выполнен вход в систему')
			sleep(1)
			return redirect(url_for('user', name=session.get('username', None) ))
			# return render_template('login.html', form=form, data='вход выполнен')
		else:
			flash('логин или пароль неверны')
			flash('возможно, такой пользователь не зарегистрирован')
			return render_template('login.html', 
				form=form, data=session.get('username', None) )
	return render_template('login.html', form=form, data=session.get('username', None)) #   V
	#  пока форма не пройдет валидацию, значение переменной будет None

@app.route('/signin', methods=('GET', 'POST')) 
def signin():
	form = SigninForm()
	if form.validate_on_submit():
		session['username'] = form.username.data
		session['pas'] = form.password.data 
		# if User.query.filter(User.username == form.username.data).first() or User.query.filter(User.email == form.email.data).first(): логич ИЛИ
		# if User.query.filter_by(username=form.username.date).filter_by(email=form.email.data).first():		связываются логическим И
		if User.query.filter( (User.username==form.username.data) | (User.email==form.email.data) )[:]: 	# логич ИЛИ
			flash("пользователь с таким именем или email уже существует")
			return render_template('signin.html', form=form, msg="используй другие данные для регистрации")

		usr = User(username=form.username.data, password_hash=form.password.data, email=form.email.data)
		db.session.add(usr)
		db.session.commit()
		return redirect(url_for('login')) 
	return render_template('signin.html', form=form, msg=None)


@app.route('/logout', methods=('GET', 'POST'))
def logout():
	form = LogoutForm()
	if form.validate_on_submit():
		session['username'] = None
		session['pas'] = None
		session['email'] = None
		return redirect(url_for('about_me'))
	return render_template('logout.html', form=form, title='выход из аккаунта')

# total chat


@app.route('/submit_form', methods=('GET', 'POST'))
def submit_form():
	form = MyForm()
	if form.validate_on_submit():
		return redirect(url_for(submit_redir))
	return render_template('submit_form.html', 
		form=form, title='вход')

@app.route('/submit_redir')
def submit_redir():
	return redirect('<h2>you write: %s</h2>' % form.name)

@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo(): 
	form = PhotoForm() 
	if form.validate_on_submit():
		f = form.photo.data		
		filename = secure_filename(f.filename) 
		filename = f.filename
		f.save(os.path.join(app.instance_path, 'photo', filename))
		return redirect(url_for('upload_photo'))
	return render_template('upload_photo.html', form=form)

# ----------------------------------
@app.route('/my_example')
@app.route('/example') 
def example():
	di = {'user':'drew', 'user2':'ven'}
	return render_template('example.html', dictionary=di) 
# как видно, можно навешивать несколько декораторов на одну ф. представления

# ---------------------------------

@app.route('/bootstrapfaq')
def bootstrapfaq():
	return render_template('old/faq.html')

# ---------------------------------------------

@app.route('/emptyjpg')
def emptyjpg():
	return render_template(url_for('static', filename='empty.jpg') ) 

# ------------------------------------

from flask import send_from_directory
@app.route('/download')
def send_file():
	return send_static_file(os.path.join(app.root_path, 'static'), 'drew.jpg')
	# return send_from_directory(os.path.join(app.root_path, 'static'),
		# 'drew.jpg')

@app.route('/403_error')
def img403():
	return send_from_directory(
		os.path.join(app.root_path, 'static'), '403.png')
# ------------------------------------

from app._wtForms import RecaptchaForm

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'public'	# required
app.config['RECAPTCHA_PRIVATE_KEY'] = 'private'	# required
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}

@app.route('/recaptcha')
def recaptcha():
	form = RecaptchaForm() 
	if form.validate_on_submit():
		flash('подтверждено')
		return render_template(url_for('recaptcha'))
	return render_template('capcha.html', form=form)

# https://stackoverflow.com/questions/31093964/recaptcha-public-key-config-not-set-with-flask-wtforms
# -----------------------------------

# if __name__ == '__main__':
	# app.run(host=None, port=None, debug=None, **options)
	# app.run()
	# app.run(debug=True)
	
	


# ф. make_response() принимает 1, 2 или 3 аргумента и возвращает
# объект Response, который можно возврщатаь функциями представления

# ф. redirect() принимает в качестве аргумента абсолютный или 
# отностельный url. прим:
# redirect('/index') redirect('http://www.yandex.com')

# url_for('index') вернет '/'
# url_for('index', _external=True) вернет абсолютный адрес (http://...)
# относительные исп. для организации связей между маршрутами внутри прил.
# абсолютные - для ссылок, исп. за пределами прил.

# динамич. url генерир/ с помощью url_for(), передавая ей именованные арг
# пример:
# url_for('user', name='andrew', _external=True) вернет
# http://localhost:5000/user/andrew
# любые аргументы эта ф. добавит в строку запроса:
# url_for('index', page=2) вернет /?page=2

# у дукораторов @app.errorhandler(<exit_code>)
# есть аргумента, который передается декорируемой функции как
# переменная   e   . И у этой переменной есть некоторые свойства:
# e.description

# чтобы узнать др. возможности, в т.ч. регистрация декораторов и
# какие есть декораторы в flask, контексты, возможности работы
# с сессиями, задать длительность сессии, включить логгирование
# ошибок, кодирование в json и декодирование, ajax, ... вызови help(app)
# например: 
# проверить есть ли папка для статики: app.has_static_folder (вернет True\Fals)
# поменять папку для статики можно так static_folder = 'new_abs_path_to_folder' 
# поменять путь для статики можно так: app.static_url_path = '/<hew_path>'

# flask реализует встроенную поддержку всплывающих сообщений:
# from flask import flash
# во вьюшке:
# flash(<сообщение>)
# а в шаблоне используй ф. get_flashed_messages что-то в роде:
# {% for message in get_flashed_messages() %}
# 	<div class="alert info-warning">
# 		<button type="button" class="close" data-dismiss="alert">&time;</button>
# 		{{ message }}
# 	</div>
# {% endfor %}

# в flask wtf формы по умолчанию защищаются csrf защитой
# но ее можно отключить 2 путями:
# 1 отдельно для формы:
# form = FlaskForm(csrf_enabled=False)
# 2 глобально для всех форм
# WTF_CSRF_ENABLED = False
# 	для генерирования csrf токена, нужно иметь секретный ключ, 
# по умолчанию, берется тот же секретный ключ, который мы задаем
# нашему приложению, но его можно сделать другим:
# WTF_CSRF_SECRET_KEY = 'рандомная строка'

# validate_on_submit() эквивалентно form.is_submitted() and form.validate()

# form = PhotoForm()
# эквивалентно этому:
# from flask import request
# from werkzeug.datastructures import CombinedMultiDict
# form = PhotoForm(CombinedMultiDict((request.files, request.form)))



# (! :D ) кажется я нашел как можно скачивать данные с сервака
# import os
# from flask import send_from_directory
# @app.route('/some_url')
# def send_file():
# 	return send_from_directory(os.path.join(app.root_path, 'static'),
# 		'<some_file>')	# , mimetype='image')
# можно не добавлять mimetype, тип файла определится автоматически
# но можно добавить

# если сделать такое условие:
# if request.method == 'POST': ...
# то можно обрабатывать формы с post запросом, но насоклько
# это безопасно я не знаю
# при form.validate_on_submit() по крайней мере проверяются
# валидаторы


# 	хеширование паролей
# from werkzeug.security import generate_password_hash, check_password_hash
#	 в pas_hash запишется хеш пароля
# pas_hash = generate_password_hash('myPassword')
# 	везвращает True или False 
# check_password_hash(pas_hash, 'myPassword')