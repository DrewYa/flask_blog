from flask_wtf import FlaskForm,  RecaptchaField
from wtforms import (StringField, PasswordField, BooleanField,
	SubmitField)
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
	confirm = PasswordField('подтверди пароль', validators=[
		EqualTo('password', message='пороли не совпадают')])
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
	submit = SubmitField('войти')

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