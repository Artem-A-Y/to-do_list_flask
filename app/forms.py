# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class InputLoginForm(FlaskForm):

    username = StringField('Username*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationLoginForm(FlaskForm):

    username = StringField('Username*', validators=[DataRequired()])
    email = StringField('E-mail*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired(), EqualTo('password_repeat')])
    password_repeat = PasswordField('Repeat Password*', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('User with this name already exists*')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('User with this email already exists*')


class AddTask(FlaskForm):

    mission = TextAreaField('Описание*', validators=[Length(min=0, max=255), DataRequired()])
    date_start = DateField('Начало*', validators=[DataRequired()])
    date_the_end = DateField('Конец*', validators=[DataRequired()])
    submit = SubmitField('Add')

