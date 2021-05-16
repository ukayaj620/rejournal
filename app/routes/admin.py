from flask import Blueprint, render_template
from flask_login import login_required
from app.middlewares.role_checker import RoleChecker

admin = Blueprint('admin', __name__, template_folder='templates')
role_checker = RoleChecker()

@admin.route('/', methods=['GET'])
@login_required
@role_checker.check_permission(role='admin')
def index():
  return render_template('pages/index.html', role='Admin')
