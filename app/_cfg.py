# элементы конфигурации могут быть доступны в основном приложении
# со словарным синтаксисом:
# app.config['SECRET_KEY'] = 'blamblambanan'
# а можно сделать конфигурацию в отдельном классе и поместить ее даже
# в отдельный файл например, в этот файл - cfg.py:

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'blamblambanan' # (1)
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')	# (2)
	SQLALCHEMY_TRACK_MODIFICATIONS = False # (3)

class ConfigWithDebug(Config):
	DEBUG = True

class ConfigWithErrorToGmail(Config):		#2041
	MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)  # 465, 25, 587
	MAIL_USE_TLS = True # os.environ.get('MAIL_USE_TLS') is not None 
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # or <мой ящик на gmail> 
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # or <мой пароль от ящика на gmial> 
	ADMINS = os.environ.get('TO_MAILS').split(',') 
	# в cmd нужно будет устанавливать из-под вирт окр, примерно так:
	# (venv) $ set TO_MAILS=ex1@example.com ex2@example.com ex3@example.com 
	# т.е. просто через запятую (без кавычек и пробелов)
	#	 (!) нужно разрешить отправлять с ненадежных приложений:
	# https://support.google.com/accounts/answer/6010255?hl=en
	# для гугл-почты без авторизации сообщения не будут отправляться

class ConfigWithErrorToEmail(Config):
	MAIL_SERVER = os.environ.get('MAIL_SERVER')     or 'smtp.mail.ru' # smtp.list.ru / smtp.bk.ru / smtp.inbox.ru
	MAIL_PORT = int(os.environ.get('MAIL_PORT')     or 465) # 465, 25, 587
	MAIL_USE_TLS = True # os.environ.get('MAIL_USE_TLS') is not None   # True - флаг вкл зашифр. соединения
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # необязательное
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # необязательное
	ADMINS = os.environ.get('TO_MAILS').split(',')  # список из адресов, - на все эти адреса будут приходить отчеты




# позже можно добавлять другие параметры конфигурации в этот класс
# а если нужно будет другие конфигурации, то можно унаследовать
# их от этого класса и позже импортировать в основное приложение

# (1) flask и некоторые его расширения используют значение секретного ключа
# в качестве криптографического ключа, полезного для генерации подписей
# или токенов.   	Например, flask-wtf (надстройка над пакетом wtforsm)
# по умолчанию использует его для защиты веб-форм атак 
# cross-site request forgery (CSRF)
# здесь - значение выражения ключа задается двумя терминами: первый ищет
# SECRET_KEY в переменной окружения, второй - просто строка


# касательно app.config в основном приложении:
# app.config.from_pyfile('config.cfg', silent=False)
# или
# app.config.from_object(obj)	# для нашего случая хорошо подойдет
# в обоих случаях нужно писать ключи конфигурации прописными буквами
# чтобы они были добавлены в конфигурацию, что делает возможным писать
# ключи с маленькой буквы прозапас
# или 
# app.config.from_envvar(variable_name, silent=False)
# прим: app.config.from_pyfile(os.environ['<SOME_SETTING>'])
# app.config.from_json(filename, silent=False)
# app.config.from_mapping(*mapping, **kwards)
	
# .get_namespace(namespace, lowercase=True, trim_namespace=True)
# возвращает словарь, содержащий опции конфигурации
# image_store_config = app.config.get_namespace('IMAGE_STORE_')
# вернет
# {
#     'type': 'fs',
#     'path': '/var/app/images',
#     'base_url': 'http://img.website.com'
# }
# если конфигурация была такая:
# app.config['IMAGE_STORE_TYPE'] = 'fs'
# app.config['IMAGE_STORE_PATH'] = '/var/app/images'
# app.config['IMAGE_STORE_BASE_URL'] = 'http://img.website.com'

# .copy()
# .delete()
# .pop()
# .items()
# .keys()
# .get()
# .values()

# =====================================

# (2) указываем путь к БД, и ее имя (в нашем случае app.db)
# (3) отключаем сигнализирование об изменениям в БД

# ====================================

#2041

# SMTP - протокол передачи электронной почти в сетях TCP/IP
# с 2008 есть ESMTP (Extended). Сейчас под SMTP обычно понимают
# и его расширения

# SMTP используется для отправки сообщения,
# а POP или IMAP - для получения
# изначально SMTP не требовала аутентификации, и эту возможность
# добавили только в расширениях
# Порты для безопасной передачи: 25 (стандартный), 587
# для неащищенной передачи: 2525
# другие: 465 (mail.ru с шифрованием)
# 	Для mail.ru 	https://help.mail.ru/mail-help/mailer/popsmtp
# сервер исходящей корреспонденции – smtp.mail.ru; 
# имя юзера – полное название зарегистрированного в сервисе адреса электронной почты; 
# пароль – парль для входа в ящик; 
# порт при выборе протокола шифрования SSL/TLS – 465 
# 	Для yandex.com 
# сервер исходящей корреспонденции smtp.yandex.ru 
# для порта указывается значение 465, но в настройках защиты устанавливается исключительно TLS
# остальное - аналогично
# 	gmail
# адрес сервера: smtp.gmail.com; 
# логин: адрес электронной почты; 
# пароль: ваш пароль Gmail; 
# порт (TLS): 587; 	 порт (SSL): 465; 
# требуется Gmail SMTP TLS/SSL: да. 
# (!) В дополнение к этим настройкам SMTP Gmail (ipb 3.4.6) вы должны 
# разрешить почтовому клиенту получать/загружать почту из аккаунта Gmail.

# http://fb.ru/article/258458/smtp-server-dlya-rassyilki-kak-nastroit-smtp-server

# (!) нужно разрешить отправлять с ненадежных приложений:
# https://support.google.com/accounts/answer/6010255?hl=en
# настройки для разных серверов:
# https://www.epochta.ru/help/mailer/09_smtp.htm