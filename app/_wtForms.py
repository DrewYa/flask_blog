from flask_wtf import FlaskForm,  RecaptchaField
from wtforms import (StringField, PasswordField, BooleanField,
	SubmitField, TextAreaField)
from wtforms.validators import (DataRequired,  Length, 
	EqualTo, Email, Optional, ValidationError)

# from wtforms.validators import FileRequired
from flask_wtf.file import FileField # , FileRequired

from app._models_bd import User

class MyForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])

class PhotoForm(FlaskForm):
	submit = SubmitField('подтвердить')
	photo = FileField(label='выбери картинку') #, validators=[FileRequired()])

# 3 класса, представляющие собой типы полей для этой формы
# импортируются прямо из wtforms. Для каждого поля объект
# создается как переменная класса в классе LoginForm
# валидаторы:
# DataRequired - проверяет, что поле не отправлено пустым
 
class LoginForm(FlaskForm):
	username = StringField('Имя пользователя', 
		validators=[DataRequired(message='имя не введено')],
		description='придумай имя',) #_translations=True)
	password = PasswordField('Пароль', validators=[
		Length(min=4, message='не короче 4 символов')])
	# confirm = PasswordField('подтверди пароль', validators=[		# убран с v6.4
	# 	EqualTo('password', message='пороли не совпадают')])
	submit = SubmitField('войти')
	remember_me = BooleanField(label='запомнить меня',
		description='ses', default=True, validators=[Optional()] )

# полям можно задавать не только label и список валидаторов,
# подробнее help(StringField) или help(PasswordField), ...
# также можно проверить какие опции можно задавать самим валидаторам
# например, сообщения об ошибке и др

class LogoutForm(FlaskForm):
	submit = SubmitField('выйти')

class SigninForm(FlaskForm):
	username = StringField('Имя пользователя', 
		validators=[DataRequired(message='имя не введено')],
		description='имя будет служить ником',) #_translations=True)
	email = StringField('email', 
		validators=[Email(message='некорректный email')])
	password = PasswordField('Пароль', validators=[
		Length(min=4, message='не короче 4 символов')])
	confirm = PasswordField('подтверди пароль', validators=[
		EqualTo('password', message='пороли не совпадают')])
	submit = SubmitField('зарегистрироваться')

	# когда мы создаем каке либо м., соответсвующие шаблону validate_<имя_поля>,
	# то wtforms примет их как пользовательские валидаторы и вызывает их в 
	# дополнение к стандартым валидаторам
	def validate_username(self, username):		# дописал 2 проверки в v5.1
		usr = User.query.filter(User.username==username.data).first()
		if usr is not None:
			raise ValidationError('Это имя уже занято, используйте другое')

	def validate_email(self, email):
		usr = User.query.filter(User.email==email.data).first()
		if usr is not None:
			raise ValidationError('Этот email уже используется для учетной записи')

# from uuid import uuid4

class EditProfileForm(FlaskForm):
	username = StringField('Имя пользователя', validators=[DataRequired(message='имя не введено')],
		description='здесь можно ввести новый псевдоним')
	about_me = TextAreaField('Немного обо мне', validators=[
		Length(min=0, max=240, message='не больше 240 символов')],
		description='мои увлечения, чем занимюсь, интересности')
	# avatar_random = uuid4().hex
	# avatar_random = StringField('генерация нового аватара', description="введи любые символы для генерации аватара",
	# 	validators=[Optional(), Length(min=12, message="минимум 12 любых символов")])
	submit = SubmitField('сохранить')
	# avatar
	# username
	# password
	# confirm
	# current_password
	
	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			usr = User.query.filter(User.username==self.username.data).first()
			if usr is not None:	# if user:
				raise ValidationError('Это имя уже занято')

class PostForm(FlaskForm):
	post = TextAreaField('Напиши что-нибудь', validators=[
		Length(min=1, max=140, message='допустимо от 1 до 140 символов')],
		description='Я хочу сказать, что ...')
	submit = SubmitField('запостить')


class RecaptchaForm(FlaskForm):
	recaptcha = RecaptchaField()
	submit = SubmitField('подтвердить')


# например для строкового поля (лишь часть документации):
# __init__(self, label=None, validators=None, filters=(), description='', id=None, default=None, widget=None, render_kw=None, _form=None, _name=None, _prefix='', _translations=None, _meta=None)
#  |      Construct a new field.
#  |
#  |      :param label:
#  |          The label of the field.
#  |      :param validators:
#  |          A sequence of validators to call when `validate` is called.
#  |      :param filters:
#  |          A sequence of filters which are run on input data by `process`.
#  |      :param description:
#  |          A description for the field, typically used for help text.
#  |      :param id:
#  |          An id to use for the field. A reasonable default is set by the form,
#  |          and you shouldn't need to set this manually.
#  |      :param default:
#  |          The default value to assign to the field, if no form or object
#  |          input is provided. May be a callable.
#  |      :param widget:
#  |          If provided, overrides the widget used to render the field.
#  |      :param dict render_kw:
#  |          If provided, a dictionary which provides default keywords that
#  |          will be given to the widget at render time.
#  |      :param _form:
#  |          The form holding this field. It is passed by the form itself during
#  |          construction. You should never pass this value yourself.
#  |      :param _name:
#  |          The name of this field, passed by the enclosing form during its
#  |          construction. You should never pass this value yourself.
#  |      :param _prefix:
#  |          The prefix to prepend to the form name of this field, passed by
#  |          the enclosing form during construction.
#  |      :param _translations:
#  |          A translations object providing message translations. Usually
#  |          passed by the enclosing form during construction. See
#  |          :doc:`I18n docs <i18n>` for information on message translations.
#  |      :param _meta:
#  |          If provided, this is the 'meta' instance from the form. You usually
#  |          don't pass this yourself.
#  |
#  |      If `_form` and `_name` isn't provided, an :class:`UnboundField` will be
#  |      returned instead. Call its :func:`bind` method with a form instance and
#  |      a name to construct the field.

# ===================================

# у валидаторов поменьше параметров:
# DataRequired(message=...)
# Length(message=..., min=None, max=None)
# Email(message=...)
# EqualTo(fieldName=<field>, message=...)
# FileRequired(message=...)

# =================================

# как работать с валидатором FormSelect

# делаем поле опциональным (необязательным), это будет форма выбора
# из нескольких предложенных вариантов
# class FormChoice():
# 	myfield = SelectField('myfield', validators=[Optional()])
# 	submit = SubmitField()
# 	можно задавать варианты выбора прямо в классе:
# 	choices = (('', ''), ('1', "first variable"), ('2', "second")) 

# или сделать во вьюшке. делаем:
# form = myform(csrf_enabled=False)
#     form.myfield.choices = (('', ''), ('apples', 'apples'), ('pears', 'pears'))

# if not form.validate():
#       return search_with_no_parameters()
# else:
#       return search_with_parameters(form) 

# --------

# есть еще:
# form.is_submited()