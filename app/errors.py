from flask import render_template
from app import app, db


# как и ф. представления, обработчики ошибок возвращают ответ с 
# числовым кодом состояния
@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404

@app.errorhandler(403)
def not_permission(e):
	return render_template('403.html'), 403

@app.errorhandler(500)
def internal_server_error(e):
	db.session.rollback() 	# если возникает ошибка, то откатываем незакомиченные изменения в сессии
	# любопытно, что без отката, будет отображаться не кастомная, а
	# стоковая страница для этой ошибки. Хотя по отношению к записям в
	# БД нет разницы (если еще раз зайти на стр. редактирования 
	# и попробовать изменить что-то, то все получится) 
	return render_template('500.html'), 500


import logging	# (1, 2, 3)
from logging.handlers import SMTPHandler # (1)
from logging.handlers import RotatingFileHandler # (2)
import os # (2)

if not app.debug:						
	if app.config['MAIL_SERVER']:		# (1) 	#2974
		auth = None
		if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
			auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
		secure = None
		if app.config['MAIL_USE_TLS']:
			secure = ()
		mail_handler = SMTPHandler(
			mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
			fromaddr='no-reply@' + app.config['MAIL_SERVER'],
			toaddrs=app.config['ADMINS'], subject='flask_blog error',
			credentials=auth, secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)
	# fromaddr - будет таким, если мы не залогинились

	if not os.path.exists('logs'):		#(2)
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/flask_blog.log',
		maxBytes=10240, backupCount=10)
	file_handler.setFormatter(logging.Formatter(
		'\n{}\n%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]\n{}\n'.format(
			' -'*25, ' -'*25)))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler (file_handler)

	app.logger.setLevel(logging.INFO) 	#(3)
	app.logger.info('flask_blog startup')




# ===================================================================
#2974

# https://ru.stackoverflow.com/questions/230/Как-посмотреть-значение-переменной-окружения-в-windows
# настройка майлсервера для mail.ru
# https://otvet.mail.ru/question/79117054

# чтобы проверить, можно запустить второй терминал и ввести в него:
# (venv) $ python -m smtpd -n -c DebuggingServer localhost:8025
# (!) в переменной конфигурации установи MAIL_SERVER = 'localhost'
# и MAIL_PORT = 8025
# вообще можно установить любой удобный порт

# =============================================
# (1) отправляем лог по почте
# (2) класс RotatingFileHandler удобен, т.к. переписывает журналы 
# 	(можно установить размер)
# 	создаем папку для файла лога (если не было), создаем лог файл,
# 	максимальная длина файла - 10 кБайт
# 	и храним последние 10 журналов в папке в качестве резервных копий

# (3) выводим сообщение о запуске сервера и
# 	выводим сообщения логгера в терминал