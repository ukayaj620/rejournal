from flask import Blueprint, request, render_template
from app.controllers.auth import AuthController

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    remember = True if request.form.get('remember') else False
    return AuthController.login(request=request.form, remember=remember)
  elif request.method == 'GET':
    return render_template('auth/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    return AuthController.register(request=request.form)
  elif request.method == 'GET':
    return render_template('auth/signup.html')

