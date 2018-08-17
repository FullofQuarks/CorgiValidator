from flask import flash, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
from . .models import User
from . import main
from .forms import LoginForm, RegisterForm, CorgiForm

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('main.login', **request.args))
        login_user(user, form.remember_me.data)
        flash('Logged in!', 'success')
        return redirect(request.args.get('next') or url_for('main.protected'))
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        User.register(form.username.data, form.password.data, '12345678')
        return redirect(url_for('main.login'))
        flash('Registration successful! Login with your newly created account')
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'dark')
    return redirect(url_for('main.index'))


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/protected', methods=['GET', 'POST'])
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

