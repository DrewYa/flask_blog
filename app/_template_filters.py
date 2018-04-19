class Filters():
	# инвертирует строку
	@app.template_filter()
	def reverse(s):
		return s[::-1]

# ----------------или--------------
def func():
	pass

app.add_template_filter(func, name="myFilter")