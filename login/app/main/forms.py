from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import Required, Length, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(1, 16)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Register')
    def validate_password(form, field):
        if form.password.data != form.confirm.data:
            flash('warning', 'Registration unsuccessful: Passwords must match')

class CorgiForm(FlaskForm):
    certificate = StringField('Certificate Number', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_certificate(form, field):
        if len(field.data) != 8:
            raise ValidationError('Certificate must be exactly 8 digits long.')

