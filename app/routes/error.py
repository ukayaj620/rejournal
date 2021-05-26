from flask import Blueprint, render_template

error = Blueprint('error', __name__, template_folder='templates')

@error.route('/unauthorized', methods=['GET'])
def unauthorized():
  return render_template('error/error.html', error_msg="401 | Unauthorized")


@error.route('/bad-request', methods=['GET'])
def bad_request():
  return render_template('error/error.html', error_msg="400 | Bad Request")