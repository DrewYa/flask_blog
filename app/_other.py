# все примеры есть здесь
# http://flask.pocoo.org/docs/0.12/api/



# в ф. описываются дейтсвия, которые будут выполняться после
# каждого запроса

def func():
	pass

app.after_request(func)


# ------или-------------
app. after_request_func = func()


-------------------------------
