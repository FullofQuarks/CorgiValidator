from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import Required, Length, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    login_required, current_user

app = Flask(__name__)
# Replace the following secret key with your own!!
app.config['SECRET_KEY'] = 'w|;$Aonru00;8A3y02+&{#oO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'login'


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

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cert = db.Column(db.String(128))
    logged = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, password, cert):
        user = User(username=username, cert=cert, logged=0) 
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def __repr__(self):
        return '<User {0}>'.format(self.username)

def logCert():
    __tablename__ = 'users'
    user = User.query.filter_by(username=current_user.username).first()
    user.logged = 1
    db.session.commit()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('login', **request.args))
        login_user(user, form.remember_me.data)
        flash('Logged in!', 'success')
        return redirect(request.args.get('next') or url_for('protected'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        User.register(form.username.data, form.password.data, '12345678')
        return redirect(url_for('login'))
        flash('Registration successful! Login with your newly created account')
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'dark')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/protected', methods=['GET', 'POST'])
@login_required
def protected():
    form = CorgiForm()
    user = ""
    valid = 0
    if form.validate_on_submit():
        if current_user.cert == form.certificate.data:
            valid = 1
            logCert()
    return render_template('protected.html', form=form, valid=valid)


if __name__ == '__main__':
    db.create_all()
    if User.query.filter_by(username='user').first() is None:
        User.register('user', 'corgi', '12345678')
    app.run(debug=True)
