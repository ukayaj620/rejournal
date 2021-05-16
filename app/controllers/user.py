from flask import redirect, url_for
from app.models.user import User


class UserController:
  
  def __init__(self):
    self.user = User()

  def update_profile_data(self, request, user_id):
    self.user.update(
      name=request['name'],
      email=request['email'],
      telephone=request['telephone'],
      gender=request['gender'],
      id=user_id
    )

    return redirect(url_for('base.profile'))

