from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

from stepik_delivery import app

csrf = CSRFProtect(app)


class RegisterForm(FlaskForm):
    mail = StringField("Электропочта", [InputRequired(), Email(message="Введите корректный адрес электропочты")])
    password = PasswordField("Пароль", [InputRequired(),
                                        Length(min=8, message="Пароль должен быть не менее 8 символов")])


class LoginForm(FlaskForm):
    mail = StringField("Электропочта", [InputRequired(), Email(message="Введите корректный адрес электропочты")])
    password = PasswordField("Пароль", [InputRequired(),
                                        Length(min=8, message="Пароль должен быть не менее 8 символов")])


class OrderForm(FlaskForm):
    name = StringField("Ваше имя", [InputRequired(message="Укажите ваше имя")])
    address = StringField("Адрес", [InputRequired(message="Укажите ваш адрес")])
    mail = StringField("Электропочта", [InputRequired(message="Укажите вашу электронную почту"),
                                        Email(message="Введите корректный адрес электропочты")])
    phone = StringField("Телефон", [InputRequired(message="Укажите ваш телефон")])
