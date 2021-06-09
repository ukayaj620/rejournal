from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.controllers.auth import AuthController
from app.controllers.journal import JournalController
from app.controllers.topic import TopicController
from app.middlewares.role_checker import RoleChecker


reviewer = Blueprint('reviewer', __name__, template_folder='templates')
role_checker = RoleChecker()
journal_controller = JournalController()
topic_controller = TopicController()

@reviewer.route('/', methods=['GET'])
@login_required
@role_checker.check_permission(role='reviewer')
def index():
  return render_template('pages/index.html', role='Reviewer')


@reviewer.route('/manuscript/submission', methods=['GET'])
@login_required
@role_checker.check_permission(role='reviewer')
def manuscript_submission():
  manuscripts = journal_controller.fetch_by_status(status='Submitted')
  topics = topic_controller.fetch_all()
  return render_template('pages/reviewer/manuscript/submission.html', role='Reviewer', manuscripts=manuscripts, topics=topics)


@reviewer.route('/manuscript/download/<filename>', methods=['GET'])
@login_required
@role_checker.check_permission(role='reviewer')
def manuscript_download(filename):
  return journal_controller.download(filename)


@reviewer.route('/manuscript/detail/<id>', methods=['GET', 'POST'])
@login_required
@role_checker.check_permission(role='reviewer')
def manuscript_view_detail(id):
  manuscript = journal_controller.fetch_by_id(journal_id=id)
  topics = topic_controller.fetch_all()
  return render_template(
    'pages/reviewer/manuscript/detail.html', 
    role='Reviewer', 
    topics=topics, 
    manuscript=manuscript,
    back_endpoint=request.form['path'],
    back_text=request.form['breadcrumb']
  )


@reviewer.route('/manuscript/review/list', methods=['GET'])
@login_required
@role_checker.check_permission(role='reviewer')
def manuscript_review_list():
  manuscripts = journal_controller.fetch_by_reviewer()
  statuses = [status for status in journal_controller.status.query.all() if status.name != 'Submitted']
  return render_template('pages/reviewer/manuscript/review.html', role='Reviewer', statuses=statuses, manuscripts=manuscripts)


@reviewer.route('/manuscript/review', methods=['POST'])
@login_required
@role_checker.check_permission(role='reviewer')
def manuscript_review():
  journal_controller.review(request=request.form)
  return redirect(url_for('reviewer.manuscript_review_list'))


@reviewer.route('/manuscript/reject', methods=['POST'])
@login_required
@role_checker.check_permission(role='reviewer')
def manuscript_reject():
  journal_controller.reject(request=request.form)
  return redirect(url_for('reviewer.manuscript_review_list'))


@reviewer.route('/manuscript/accept', methods=['POST'])
@login_required
@role_checker.check_permission(role='reviewer')
def manuscript_accept():
  journal_controller.accept(request=request.form)
  return redirect(url_for('reviewer.manuscript_review_list'))

