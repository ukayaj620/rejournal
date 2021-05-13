from flask import flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from datetime import timedelta
import random
import string
from app.models.user import User
from app.models.verification import Verification
from app.utils.mailer import send_signup_verification
from app.utils.time import is_expire


class AuthController:

  @staticmethod
  def sent_verification_email(email, msg='', reset=False):
    fetched_user = User.query.filter_by(email=email).first()

    token = ''.join(random.choice(string.ascii_letters) for i in range(20))
    link = f'{fetched_user.id}/{token}'

    hashed_token = generate_password_hash(token, method='sha256')

    if reset:
      Verification.update(Verification, token=hashed_token, user_id=fetched_user.id)
    else:
      Verification.create(Verification, token=hashed_token, user_id=fetched_user.id)

    send_signup_verification(to=fetched_user.email, link=link)

    flash(f'{msg}. Verification link has been sent to your email, please check it out', 'info')
    return redirect(url_for('auth.email_verification', email=email))

  @staticmethod
  def login(request, remember):
    user = User.query.filter_by(email=request['email']).first()

    if not user:
      flash('Please check your login details and try again.', 'danger')
      return redirect(url_for('auth.login'))

    if bool(user.is_verified) == False:
      return AuthController.sent_verification_email(email=request['email'], msg='Your email has not been verified', reset=True)

    if not check_password_hash(user.password, request['password']):
      flash('Please check your login details and try again.', 'danger')
      return redirect(url_for('auth.login'))

    login_user(user, remember=remember, duration=timedelta(days=30))
    return redirect(url_for('home.index'))

  @staticmethod
  def register(request):
    user = User.query.filter_by(email=request['email']).first()
    if user:
      flash('Email has already existed', 'warning')
      return redirect(url_for('auth.signup'))

    user = User.query.filter_by(telephone=request['telephone']).first()
    if user:
      flash('Telephone has already existed', 'warning')
      return redirect(url_for('auth.signup'))

    User.create(
      name=request['name'],
      email=request['email'],
      telephone=request['telephone'],
      gender=request['gender'],
      password=generate_password_hash(request['password'], method='sha256')
    )

    return AuthController.sent_verification_email(email=request['email'])

  @staticmethod
  def verify(token, user_id):
    verification = Verification.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(id=user_id).first()

    if not token or\
      not check_password_hash(verification.token, token) or\
      is_expire(expire=verification.valid):
      flash('Link has expire, request for other link', 'warning')
      return redirect(url_for('auth.email_verification', email=user.email))

    User.verified_user(id=user_id)
    Verification.delete(Verification, token_id=verification.id)
    
    flash('Your account has been verified, please login', 'info')
    return redirect(url_for('auth.login'))

  @staticmethod
  def logout():
    logout_user()
    return redirect(url_for('auth.login'))

