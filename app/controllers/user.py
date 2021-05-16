from flask import redirect, url_for
from app.models.user import User
from app.utils.image import save_image, delete_image


class UserController:
  
  def __init__(self):
    self.user = User()

  def get_profile(self, user_id):
    return self.user.query.filter_by(id=user_id).first()

  def update_profile_data(self, request, user_id):
    self.user.update(
      name=request['name'],
      email=request['email'],
      telephone=request['telephone'],
      gender=request['gender'],
      id=user_id
    )

    return redirect(url_for('base.profile'))

  def update_profile_image(self, photo, user_id):
    user = self.get_profile(user_id=user_id)

    filename = save_image(photo) if photo else None
    delete_image(user.picture_path) if filename is not None else None

    self.user.update_image(
      filename=filename,
      id=user_id
    )

    return redirect(url_for('base.profile'))
