from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username=StringField("Usuario", validators=[DataRequired()])
    password=PasswordField("Contraseña", validators=[DataRequired()])
    remember_me=BooleanField("Recuérdame")
    submit=SubmitField("Iniciar sesión")

class SignUpForm(FlaskForm):
    username=StringField("Usuario", validators=[DataRequired()])
    email=StringField("Correo", validators=[DataRequired()])
    password=PasswordField("Contraseña", validators=[DataRequired()])
    submit=SubmitField("Registrar nuevo usuario")


class NotasForm(FlaskForm):
    name=StringField("Titulo de nota", validators=[DataRequired()])
    email=StringField("Fecha", validators=[DataRequired()])
    number=StringField("Nota", validators=[DataRequired()])
    submit=SubmitField("Guardar nota")