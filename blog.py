# экземпляр приложения импортируется из нашего пакета app
from app import app

# должна получиться такая структура:
# _blog_pachage_eigth/
#   venv/
#   app/
#     __init__.py
#     routes.py
#     templates/
#       base.html
#       index.html
#       404.html
#       500.html
#       aboutMe.html
#     static/
#       500.jpg
#       favicon.ico
#   blog.py

# хотя в моем случае папка с виртуальным окружением стоит 
# выше еще выше

# прежде чем запускать приложение нужно сообщить Flask'у
# как его импортировать, установив переменную 
# среды FLASK_APP:
# для Linux:
# (venv) $ export FLASK_APP=blog.py
# для Windows:
# (venv) $ set FLASK_APP=blog.py

# теперь можно запускать:
# (venv) $ flask run

# flask команды полагаются на переменную среды FLASK_APP,
# чтобы знать где расположено приложение Flask 

# также есть переменная среды окружения, отвечающая за включение
# дебага:		FLASK_DEBUG=1

# ----------------------------------------------
# внимание, может не заработать из-за кодировки если версия
# python 3.6 или старше
# это из-за кириллицы в имени компа
# виноват модуль socket
# исправлять так:

# >>> from socket import gethostbyaddr
# >>> gethostbyaddr('127.0.0.1')
# ('Acer-PK', [], ['127.0.0.1'])

# где Acer-PK - подставленное имя компа на английском

# ---------------------------------------------------------

# Что бы написать по русски "Привет, Мир!" потребуется скорректировать
# модуль routes.py
# Добавить строку # -*- coding: utf-8 -*-
# в самое начало файла

# --------------------------------------------
# ну и для Linux указать какой интерпретатор должен запускать 
# (не обязательно, но можно):
#!/usr/bin/env python
# ----------------------------------------

# если возникнут проблемы с html файлами, то попробуй
# сохранить их в кодировке utf-8

# =========================================

# (venv_p32_blog) c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth>flask run
# Usage: flask run [OPTIONS]

# Error: Could not locate Flask application. You did not provide the FLASK_APP environment variable.

# For more information see http://flask.pocoo.org/docs/latest/quickstart/

# (venv_p32_blog) c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth>set FLASK_APP=blog.py

# ===================================================
# flask-migrate выдает свои команды через flask команду 
# (типа как flask run, которая явл. подчиненной командой)

# flask db
# эта команда добавляется расширением flask-migrate
# для управления всем, что связано с миграцией БД

# flask db init 
# создает репозиторий миграции для блога blog 
# (выполняется однократно)

# flask db migrate 
# или
# flask db migrate -m "my comment"
# перенесет все модели в сценарий переноса
