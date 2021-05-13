from flask import flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app.models.user import User


class AuthController:

  @staticmethod
  def login(request, remember):
    user = User.query.filter_by(email=request['email']).first()

    if not user:
      flash('Please check your login details and try again.', 'danger')
      return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, request['password']):
      flash('Please check your login details and try again.', 'danger')
      return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
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

    return redirect(url_for('auth.login'))

  @staticmethod
  def logout():
    logout_user()
    return redirect(url_for('auth.login'))

