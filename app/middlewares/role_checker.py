from flask import redirect, url_for
from flask_login import current_user
import functools
from app.models.role import Role

class RoleChecker:

  def check_permission(self, role):
    def decorator_check_permission(func):
      @functools.wraps(func)
      def wrapper_check_permission(*args, **kwargs):
        role_name = Role.query.filter_by(id=current_user.role_id).first().name
        print(role_name)
        if role != role_name:
          return redirect(url_for('error.unauthorized'))

        return func(*args, **kwargs)
      
      return wrapper_check_permission
    
    return decorator_check_permission