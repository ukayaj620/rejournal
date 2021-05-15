from flask import Blueprint, render_template

home = Blueprint('home', __name__, template_folder='templates')

@home.route('/', methods=['GET'])
def index():
  return render_template('/pages/index.html', role='Home')
