from flask import Blueprint, render_template
from flask_login import login_required

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/', methods=['GET'])
@login_required
def index():
  return render_template('pages/index.html', role='User')
