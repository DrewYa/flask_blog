class Filters():
	# инвертирует строку
	@app.template_filter()
	def reverse(s):
		return s[::-1]
