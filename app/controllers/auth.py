from flask import flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from datetime import timedelta
import random
import string
from app.models.user import User
from app.models.role import Role
from app.models.verification import Verification
from app.utils.mailer import send_signup_verification
from app.utils.time import is_expire
from app.utils.cryptographic import encoder, decoder


class AuthController:

  def __init__(self):
    self.user = User()
    self.role = Role()
    self.verification = Verification()

  def get_role_name(self, role_id):
    return self.role.query.filter_by(id=role_id).first().name

  def determine_redirection(self, role_id):
    role_name = self.get_role_name(role_id=role_id)
    choice = {
      'user': 'home.index',
      'admin': 'admin.index',
      'reviewer': 'reviewer.index'
    }

    return redirect(url_for(choice.get(role_name, 'error.unauthorized')))

  def sent_verification_email(self, email, msg='', reset=False):
    fetched_user = self.user.query.filter_by(email=decoder(email)).first()

    token = ''.join(random.choice(string.ascii_letters) for i in range(20))
    link = f'{fetched_user.id}/{token}'

    hashed_token = generate_password_hash(token, method='sha256')

    if reset:
      self.verification.update(token=hashed_token, user_id=fetched_user.id)
    else:
      self.verification.create(token=hashed_token, user_id=fetched_user.id)

    send_signup_verification(to=fetched_user.email, link=link)

    flash(f'{msg}. Verification link has been sent to your email, please check it out', 'info')
    return redirect(url_for('auth.email_verification', email=email))

  def login(self, request, remember):
    user = self.user.query.filter_by(email=request['email']).first()

    if not user:
      flash('Please check your login details and try again.', 'danger')
      return redirect(url_for('auth.login'))

    if bool(user.is_verified) == False:
      if self.get_role_name(role_id=user.role_id) == 'user':
        return self.sent_verification_email(email=encoder(request['email']), msg='Your email has not been verified', reset=True)

      flash('Please renew your password!', 'info')
      return redirect(url_for('auth.update_password', email=encoder(request['email'])))

    if not check_password_hash(user.password, request['password']):
      flash('Please check your login details and try again.', 'danger')
      return redirect(url_for('auth.login'))

    login_user(user, remember=remember, duration=timedelta(days=30))
    
    return self.determine_redirection(role_id=user.role_id)

  def register(self, request):
    user = self.user.query.filter_by(email=request['email']).first()
    if user:
      flash('Email has already existed', 'warning')
      return redirect(url_for('auth.signup'))

    user = self.user.query.filter_by(telephone=request['telephone']).first()
    if user:
      flash('Telephone has already existed', 'warning')
      return redirect(url_for('auth.signup'))

    self.user.create(
      name=request['name'],
      email=request['email'],
      telephone=request['telephone'],
      gender=request['gender'],
      password=generate_password_hash(request['password'], method='sha256'),
      role_id=self.role.query.filter_by(name='user').first().id
    )

    return self.sent_verification_email(email=encoder(request['email']))

  def verify(self, token, user_id):
    verification = self.verification.query.filter_by(user_id=user_id).first()
    user = self.user.query.filter_by(id=user_id).first()

    if not token or\
      not check_password_hash(verification.token, token) or\
      is_expire(expire=verification.valid):
      flash('Link has expire, request for other link', 'warning')
      return redirect(url_for('auth.email_verification', email=user.email))

    self.user.verified_user(id=user_id)
    self.verification.delete(token_id=verification.id)
    
    flash('Your account has been verified, please login', 'info')
    return redirect(url_for('auth.login'))

  def update_password(self, request):
    print(decoder(request['email']))
    user = self.user.query.filter_by(email=decoder(request['email'])).first()
    self.user.update_password(password=generate_password_hash(request['password'], method='sha256'), id=user.id)
    self.user.verified_user(id=user.id)
    flash('Your password has been updated and account has been verified, please login', 'info')
    return redirect(url_for('auth.login'))

  def logout(self):
    logout_user()
    return redirect(url_for('auth.login'))

