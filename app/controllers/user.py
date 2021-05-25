from flask import redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
from app.models.user import User
from app.models.role import Role
from app.utils.file import save_image, delete_image
from app.utils.mailer import send_account_credential
from flask_login import current_user


class UserController:
  
  def __init__(self):
    self.user = User()
    self.role = Role()

  def fetch_user_by_role(self, role):
    role_id = self.role.query.filter_by(name=role).first().id
    return self.user.query.filter(User.id != current_user.id, User.role_id == role_id).all()

  def get_profile(self, user_id):
    return self.user.query.filter_by(id=user_id).first()

  def create(self, request, role):
    user = self.user.query.filter_by(email=request['email']).first()
    if user:
      return flash('Email has already existed', 'warning')

    user = self.user.query.filter_by(telephone=request['telephone']).first()
    if user:
      return flash('Telephone has already existed', 'warning')

    password = ''.join(random.choice(string.ascii_letters) for i in range(20))
    hashed_password = generate_password_hash(password, method='sha256')

    self.user.create(
      name=request['name'],
      email=request['email'],
      telephone=request['telephone'],
      password=hashed_password,
      gender=request['gender'],
      role_id=self.role.query.filter_by(name=role).first().id
    )

    send_account_credential(to=request['email'], password=password)
    return flash('User has been created, credentials has been sent to user.', 'info')

  def update(self, request, user_id):
    self.user.update(
      name=request['name'],
      email=request['email'],
      telephone=request['telephone'],
      gender=request['gender'],
      id=user_id
    )

  def update_profile_image(self, photo, user_id):
    user = self.get_profile(user_id=user_id)

    filename = save_image(photo)
    delete_image(user.picture_path) if user.picture_path is not None else None

    self.user.update_image(
      filename=filename,
      id=user_id
    )

    return redirect(url_for('base.profile'))

  def delete(self, user_id):
    self.user.delete(id=user_id)
