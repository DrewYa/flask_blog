from app import db # db = SQLAlchemy(app)
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	# __tablename__ = 'user' 	# (4)
	post = db.relationship('Post', backref='author', lazy='dynamic') # (1)

	def __repr__(self): 
		return '<User {}> |id: {} |email: {}'.format(
			self.username, self.id, self.email)

class Post(db.Model):
	# __tablename__ = 'post'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, 
		default=datetime.utcnow) # (2)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # (3)
	# благодаря полю post и параметру backref в нем в классе
	# User в этот (Post) класс будет добавлено поле author

	def __repr__(self):
		return '<Post {}|user_id: {} |data: {}>'.format(
			self.body, self.user_id, self.timestamp)


# ===============================================
# класс User:

# каждый экземпляр этого класса будет записью в таблице "users"
# пример создания экземпляра (т.е. добавления записи в таблицу)
# u = User(username='Drew', email='drew@site.com')

# ф. __repr__ нужна чтобы отобразить запись с помощью print()
# print(u)		даст такой результат:
# <User Drew> |id: 1 |email: drew@site.com

# каждый класс, наследуемый от db.Model - это модель таблицы
# по которой будет создана таблица (а экземпляр этого класса - 
# это запись в таблице)

# в качестве первого параметра указываем столбец, содержаций
# id записей, которые будут индексироваться при добавлении
# новых записей, а также указываем, что это значение уникально

# в 2 атрибуте указываем какой будет 2 столбец будущей таблицы
# он будет хранить значения имен пользователей, максимальная
# длина которых будет 64 символа, значения должны быть уникальными
# и это тоже индексируемой поле

# 3 атрибут - 3 столбец таблицы - электронная почта, 
# мак длина 120 символов, индексируемые записи, уникальные

# 4 атрибут - 4 столбец таблицы - хэши паролей пользователей
# все хэши имеют длину 128 символов (или 256)
# почему именно хэши, а не сами пароли?
# так надежнее, если БД будет взломана, то злоумышленник
# все равно не узнает пароли, т.к. он не зает какой хэш-функцией
# были закодированы пароли

# индексировать поля не обязательно, но это ускоряет поиск, к тому 
# же, если мы хотим получить значения в хронологическом порядке

# каждое поле - экземпляр класса db.Column()

# =========================================================

# созданный класс модели определяет исходную структуру (схему) БД
# для этого приложения. По мере расширения проекта можут понадобиться 
# изменить структуру, - добавить новые сущности или наоборот удалить
# элементы.		Для этого есть Alembic, который поможет с
# миграцией БД. Сценарии миграции будут выполнены в той последовательности
# в которой они были созданы
# Flask-Migrate - надстройка над этим пакетом
# https://habrahabr.ru/post/346344/

# ====================================================
# (1)

# поле сообщений (постов), которое инициализируется db.relationship
# Это не фактическое поле базы данных, а высокоуровневое представлени
# о взаимоотношениях между users и posts. Поэтому оно НЕ находится
# в диаграмме БД, которую мы нарисовали (на сайте в бразуере)
# Для отношений один-ко-многим db.relationship обычно определяется
# на стороне "один" и исп. как удобный способ оплучить доступ 
# ко "многим".
# Прим: если у нас есть пользователь хранящийся в usr1 - экземпляре 
# класса User, то получить все записи (посты) написанные этим 
# пользователем можно так:
# usr1.posts

# post = db.relationship('Post'<1>, backref='author' <2>, lazy='dynamic' <3>) 
# <1> класс, который представляет сторону отношения "много"
# <2> имя поля, которое будет добавлено к объектам класса "много",
# который указывает на объект "один"
# (в нашем случае добавин в табл. post поле author)
# <3> определяет как будет выполняться запрос БД для связи


# параметр backref показывает строковое имя свойства, расположенного
# в связянном классе карты (схемы), который будет обрабатывать это 
# отношение в другом направлении. Другое свойство будет создано 
# автоматически когда карта (схема) сконфигурируется. Может также 
# быть вызвано как м. backref объекта для контроля конфигурации
# нового отношения

# # -----------------
# параметр lazy - по умолчанию = 'select'
# он указывает, как должны быть загружены элементы:

# select - элементы должны быть пассивно (лениво) загружены, когда
# свойство впервые требует доступ с помощью отдельной инструкции
# SELECT состояния или с помощью карта идентификации выборки
# для простых многие-к-одному ссылок.

# immediate

# joined - ленивая загрузка - элементы должны быть загружены
# "немедленно" в тот момента, когда загружаются родительские. 
# Используется при JOIN или LEFT OUTER JOIN. 

# subquery - элемент должен быть загружен "немедленно" в том
# же момент, когда загружается родитель, используется
# 1 дополнительный оператор SQL состояния, когда запрашивает
# JOIN (присоединиться) к оригинальному состоянию, для др. 
# коллекций запросов

# selectin
# noload
# raise 
# raise_on_sql 

# dynamic - атрибут будет возвращен пре-конфигурированным объектом
# для всех операций, на которых далее фильтруемые операции могут 
# быть применены до итерирования результата. Смотри dynamic_relationship
# -------------

# (2)

# default - значение, которое будет присвоено по умолчанию полю, 
# если при создании записи оно не было указано

# обрати внимание, что utcnow мы не указали скобки в конце utcnow()
# SQLAlchemy сам установит значение которое вернет эта ф. при
# ее вызове выбранному полю (в данном случае полю timestamp), 
# но только в момент когда будет создаваться очередная запись
# (т.е. для каждой записи эта ф. будет вызываться и возвращать
# разные значения даты и времени)
# -------------------------

# (3)

# поле user_id было инициализировано как внешний ключ для user.id
# т.е. оно ссылается на значени поля id из таблицы users.
# Здесь user - это имя таблицы БД, которую flask-alchemy автоматически
# устанавливает как имя класса модели, преобразованного в нижний регистр

# (4) Но это можно исправить, если указать в классе атрибуту
# __tablename__ другое строковое значение, которое станет 
# названием таблицы




# =======================================================

# то, что выдала cmd после flask db init

# (venv_p32_blog) c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth>flask db init
# Creating directory c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth\migrations ... done
# Creating directory c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth\migrations\versions ... done
# Generating c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth\migrations\alembic.ini ... done
# Generating c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth\migrations\env.py ... done
# Generating c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth\migrations\README ... done
# Generating c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth\migrations\script.py.mako ... done
# Please edit configuration/connection/logging settings in 'c:\\Python\\virtual_envs\\venv_p32_blog\\_blog_package_eigth\\migrations\\alembic.ini' before proceeding.

# после этого появится папка migrations с файлами и папкой
# versions. Все эти файлы теперь должны рассматриваться, как
# часть проекта, 
# их нужно добавить в систему управления версиями вместе с 
# приложением (git)

# после выполнения первой миграции:
# flask db migrate -m "users table"

# (venv_p32_blog) c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth>flask db migrate -m "users table"
# INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
# INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
# INFO  [alembic.autogenerate.compare] Detected added table 'user'
# INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'
# INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_username' on '['username']'
# Generating c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth\migrations\versions\e0ccbe8cf11c_users_table.py ... done

# теперь если посмотреть созданный файл.ру то обнаружим в нем
# 2 ф.: 
# upgrade() - применяет миграцию (повышает)
#  и 
# downgrade() - удаляет ее (понижает)

# flask db migrate не вносит в БД изменений, а только
# создает сценарий миграции

# чтобы применить изменения в БД нужно выполнить 
# flask db upgrade

# (venv_p32_blog) c:\Python\virtual_envs\venv_p32_blog\_blog_package_eigth>flask db upgrade
# INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
# INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
# INFO  [alembic.runtime.migration] Running upgrade  -> e0ccbe8cf11c, users table

# т.к. я использую sqlite, команда upgrade обнаружит, что БД 
# не существует и создаст ее (файл app.db будет добавлен
# в папку пакета)
# При работе с серверами БД (MySQL, PostgreSQL) перед запуском
# обновления нужно создать БД на сервере БД

# https://habrahabr.ru/post/346344/
# =============================================

# интерактивная сессия:

# from app import db
# from app._models_bd import User, Post

# u1 = User(username='Drew', email='drew@site.org')
# db.session.add(u1)
# db.session.commit() - записать изменения в БД из сеанса

# db.session.rollback() - отменяет весь сеанс и удаляет все 
# изменения в нем

# users = User.query.all()
# print(users)

# или 

# >>> for u in users:
# ...     print(u.id, u.username)
# ...
# 1 mika
# 2 Drew

# теперь добавим первый пост
# >>> u = User.query.get(1)
# >>> u
# <User mika> |id: 1 |email: mika@j.net
# >>> p = Post(body="first post", author=u)
# >>> db.session.add(p)
# >>> db.session.commit()

# >>> Post.query.all()
# [<Post first post|user_id: 1 |data: 2018-04-15 00:46:32.258225>]

# >>> posts = u.post.all()
# >>> posts
# [<Post first post|user_id: 1 |data: 2018-04-15 00:46:32.258225>]

# >>> u2 = User.query.get(2)
# >>> u2
# <User Drew> |id: 2 |email: drew@site.org
# >>> u2.post.all()
# []

# >>> posts = Post.query.all()
# >>> for p in posts:
# ...     print(p.id, p.author.username, p.body)
# ...
# 1 mika first post

# # получить всех пользователей в обратном алфавитном порядке
# >>> User.query.order_by(User.username.desc()).all()
# [<User mika> |id: 1 |email: mika@j.net, <User Drew> |id: 2 |email: drew@site.org]

# удалим все записи из обеих таблиц
# >>> for u in  User.query.all():
# ...     db.session.delete(u)
# ...
# >>> post = Post.query.all()
# >>> for p in post:
# ...     db.session.delete(p)
# ...
# >>> db.session.commit()