# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from flask import request
from app import app, db
from app.forms import InputLoginForm, RegistrationLoginForm, AddTask
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from app.models import User, Post


@app.route('/')
@app.route('/index')
def index():
    text_on_the_page = {
                            1: 'Зарегестрироваться',
                            2: 'Войти',
                       }
    return render_template('index.html', title='To Do list application', text_on_the_page=text_on_the_page)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('to_do_list', username=current_user.username))
    form = InputLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль*')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if next_page is not None:
            next_page = next_page + '/' + current_user.username

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('to_do_list', username=current_user.username)

        return redirect(next_page)

    return render_template('login.html', title='To Do list application', form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('to_do_list', username=current_user.username))
    form = RegistrationLoginForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration was successful!')
        return redirect(url_for('login'))
    return render_template('reg.html', title='To Do Register', form=form)


@app.route('/to-do-list')
@app.route('/to-do-list/<username>', methods=['GET', 'POST'])
@login_required
def to_do_list(username):
    user = User.query.filter_by(username=username).first_or_404()
    post = Post.query.all()
    if request.method == 'POST':
        task_id = int(list(request.form)[0])
        for pos in post:
            if pos.id == task_id:
                db.session.delete(pos)
                db.session.commit()
                return redirect(url_for('to_do_list', username=current_user.username))
    return render_template('custom_to_do_list.html', user=user, post=post)


@app.route('/to-do-list/<username>/add_task', methods=['GET', 'POST'])
@login_required
def add_to_do_list(username):
    form = AddTask()
    if form.validate_on_submit():
        current_user.mission = form.mission.data
        current_user.date_start = form.date_start.data
        current_user.date_the_end = form.date_the_end.data
        u = User.query.filter_by(username=username).first_or_404()
        p = Post(mission=current_user.mission,
                 author=u,
                 timestamp_start=current_user.date_start,
                 due_date=current_user.date_the_end)
        db.session.add(p)
        db.session.commit()
        flash('Added a new task*')
        return redirect(url_for('to_do_list', username=current_user.username))
    return render_template('add_task.html', title='Add Task', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
