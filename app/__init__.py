from flask import Flask 
from app._cfg import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager

# расширения должны быть созданы и инициализированы сразу после 
# экземпляра приложения в app/init.py

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)

migrate = Migrate(app, db)

# специально импортируем внизу - это обходной путь для циклического импорта
# т.к. он должен импортировать переменную приложения (app)
# определенную в этом скрипте

# из пакета app (так назвается папка в которой находится пакет)
# импортирует модуль routes
# (пакет определяется каталогом и скриптом __init__.py)
from app import routes, _models_bd

# чтобы приложение запустилось с желаемыми параметрами:
# app.run(host='0.0.0.0', port=9079, debug=False)


# ====================================================
# >>> from app.models import User
# >>> u = User(username='susan', email='susan@example.com')
# >>> u
# <User susan>