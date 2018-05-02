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

