from flask import Blueprint, render_template
from flask_login import login_required

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/', methods=['GET'])
@login_required
def index():
  return render_template('pages/index.html', role='Admin')
