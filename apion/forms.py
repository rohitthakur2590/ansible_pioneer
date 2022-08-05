from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FieldList, FormField, TextAreaField, BooleanField, FileField, Form
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apion.models import User
from wtforms.widgets import TextArea


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirmed Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data)

        if user:
            raise ValidationError('This username is already taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data)

        if user:
            raise ValidationError('This email already exist')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class PluginDetailForm(Form):
    type = StringField('Plugin Type', validators=[DataRequired()])
    name = StringField('Plugin Name', validators=[DataRequired()])
    docstring = FileField('Docstring', validators=[DataRequired()])


class PluginBuilderForm(FlaskForm):
    dest_path = StringField('Destination Path')
    namespace = StringField('Namespace')
    coll_name = StringField('Collection Name')
    plugin_type = StringField('Plugin Type')
    plugin_name = StringField('Plugin Name')
    docstring = FileField('Docstring')
    content = TextAreaField('Content', widget=TextArea())
    first_name = TextAreaField('First Name', widget=TextArea())
    submit = SubmitField('Generate')
    reset = SubmitField('Reset')
    # pugin_type = FieldList(FormField(PluginDetailForm), min_entries=1)
    #plugins = FieldList(FormField(PluginDetailForm))




