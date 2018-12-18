import requests
import json
from flask_babel import _
from app import app

def translate(text, source_lang='en', destination_lang='ru'):
	if 'TRANSLATOR_KEY' not in app.config or\
	not app.config['TRANSLATOR_KEY']:
		return 'error' # _('Error: сервис перевода не сконфигурирован.')
	r = requests.get(
		'https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}-{}'.format(
			app.config['TRANSLATOR_KEY'], text, source_lang, destination_lang ))
	if r.status_code != 200: # or json.loads(r.text)['code'] != 200
		return 'error' # _('Error: ошибка сервиса перевода.')
	return json.loads(r.content)['text'][0]