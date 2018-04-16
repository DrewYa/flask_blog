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

# (2) указываем путь к БД 
# (3) отключаем сигнализирование об изменениям в БД
