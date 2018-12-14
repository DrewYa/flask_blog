from app import app
import click

# эта функция будет командой в терминале
# название команды бдует соответствовать названию 
# декорируемой ф.
@app.cli.group()
def translate(): 
	'''Translation  and localisation commands.'''

# теперь мы декорируем только что созданной функцией
# функцию update, которая будет являться субкомандой:
# команда в терминале: flask translate update
@translate.command()
def update():
	'''update all languages.'''
	print('как бы выполнена ф. update')
	pass

# это будет тоже субкоманда compile:
# flask translate compile
@translate.command()
def compile():
	'''compile all languages.'''
	print('как бы выполнена ф. compile')
	pass


# flask translate init <lang>
# flask translate init ru
@translate.command()
@click.argument('lang') # определяем код языка
def init(lang):
	'''initialize a new language.'''
	print('ты ввел язык: {}'.format(lang))
	pass

# Последним шагом для включения этих команд является их импорт,
#  чтобы команды регистрировались. Я решил сделать это в файле,
#  который запускает проект (в моем случае blog.py) в каталоге верхнего уровня


# теперь можно опробовать:
# flask --help
# flaks translate --help
# flaks translate compile


# =========================

# помимо команд flask run, flask shell и flask db <sub-command>
# можно добавить свои собственные команды
# Flask полагается на Click для всех своих операций с командной строкой. 
# https://click.palletsprojects.com/en/5.x/

# Они создаются с помощью декоратора app.cli.group()
# Имя команды происходит от имени декорированной функции, а справочное сообщение поступает из docstring
# Поскольку это родительская команда, которая существует только 
# для обеспечения базы для подкоманд, самой функции ничего не нужно делать.