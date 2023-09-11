# app/routes.py
from asyncio import IncompleteReadError
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from app.models import User, Todo
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

#Vorlage aus dem Unterricht, aber selbst angepasst
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
   incomplete = Todo.query.filter_by(user_id=current_user.id, complete=False).all()
   complete = Todo.query.filter_by(user_id=current_user.id, complete=True).all()
      #return redirect(url_for('index'))
   page = request.args.get('page', 1, type=int)
   return render_template('index.html', title='Home',
                      incomplete=incomplete, complete=complete)

#Codevorlage aus Somil_singh.Todo list app using Flask | Python.15.05.2020.Abgerufen von https://www.geeksforgeeks.org/todo-list-app-using-flask-python/
@app.route('/add', methods=['POST'])
def add():
    todo_item = request.form['todoitem'].strip() 
    #Eigenentwicklung
    if not todo_item:  # Check if the input is empty
        flash('Task cannot be empty!')  # Info for the User
        return redirect(url_for('index'))
    todo = Todo(body=request.form['todoitem'], complete=False, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
  
    return redirect(url_for('index'))


#Übernommen aus den Beispielen
@app.route('/explore')
@login_required
def explore():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', title='Explore', incomplete=incomplete, complete=complete)

#Übernommen aus den Beispielen
@app.route('/login', methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = LoginForm()
   if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user is None or not user.check_password(form.password.data):
         flash('Invalid username or password')
         return redirect(url_for('login'))
      login_user(user, remember=form.remember_me.data)
      next_page = request.args.get('next')
      if not next_page or url_parse(next_page).netloc != '':
         next_page = url_for('index')
      return redirect(url_for('index'))
   return render_template('login.html', title='Sign In', form=form)

#Übernommen aus den Beispielen
@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('index'))


#Übernommen aus den Beispielen
@app.route('/register', methods=['GET', 'POST'])
def register():
   if current_user.is_authenticated:
      return redirect(url_for('index'))
   form = RegistrationForm()
   if form.validate_on_submit():
      user = User(username=form.username.data, email=form.email.data)
      user.set_password(form.password.data)
      db.session.add(user)
      db.session.commit()
      flash('Congratulations, you are now a registered user!')
      return redirect(url_for('login'))
   return render_template('register.html', title='Register', form=form)

#Übernommen aus den Beispielen
@app.route('/user/<username>')
@login_required
def user(username):
   user = User.query.filter_by(username=username).first_or_404()
   page = request.args.get('page', 1, type=int)
   todos = Todo.query.filter_by(user_id=current_user.id).all()
   form = EmptyForm()
   return render_template('user.html', user=user, todos=todos,
                           form=form)

def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
   form = EditProfileForm(current_user.username)
   if form.validate_on_submit():
      current_user.username = form.username.data
      current_user.about_me = form.about_me.data
      db.session.commit()
      flash('Your changes have been saved.')
      return redirect(url_for('edit_profile'))
   elif request.method == 'GET':
      form.username.data = current_user.username
      form.about_me.data = current_user.about_me
   return render_template('edit_profile.html', title='Edit Profile', form=form)

#Eigenentwicklung
@app.route('/complete/<id>', methods=['GET','POST'])
@login_required
def complete(id):
   todo = Todo.query.filter_by(id=int(id)).first()
   todo.complete = True
   todo.timestamp = datetime.utcnow()
   db.session.commit()
    
   return redirect(url_for('index'))


#Eigenentwicklung
@app.route('/notcomplete/<id>', methods=['GET','POST'])
@login_required
def notcomplete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = False
    todo.timestamp = datetime.utcnow()
    db.session.commit()
  
    return redirect(url_for('index'))

#Eigenentwicklung
@app.route('/deletetask/<id>', methods=['GET','POST'])
@login_required
def deletetask(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

#Eigenentwicklung
@app.route('/edittask/<id>', methods=['GET', 'POST'])
@login_required
def edittask(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    if request.method == 'POST':
        # Update the task with the new data
        todo.body = request.form.get('edited_task')
        db.session.commit()
        flash('Task has been updated.')
        return redirect(url_for('index'))

    return render_template('edit_task.html', todo=todo)