from flask import Blueprint, request, render_template
from flask_login import login_required
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


@auth.route('/email-verification/<string:email>', methods=['GET'])
def email_verification(email):
  print(email)
  return render_template('auth/verification.html', data={'user_email': email})


@auth.route('/verify/<int:user_id>/<string:token>', methods=['GET'])
def verify(user_id, token):
  return AuthController.verify(token=token, user_id=user_id)


@auth.route('/resend-link', methods=['POST'])
def resend_link():
  return AuthController.sent_verification_email( 
    email=request.form['email'],
    msg='New link has been sent to your email!', 
    reset=True
  )


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
  return AuthController.logout()
